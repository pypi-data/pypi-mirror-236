# Copyright 2023 Inductor, Inc.
"""Abstractions for the Inductor CLI."""

import copy
import datetime
import importlib
import inspect
import os
from pathlib import Path
import sys
import types
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import yaml

from inductor import wire_model


class LazyCallable:
    """Container for a function or LangChain object that is lazily imported.
    
    Represents a function or LangChain object that is provided by the user as
    part of a test suite. Objects of this class are callable, and calling them
    will import the required module if necessary to call the object.

    Attributes:
        fully_qualified_name (str): Fully qualified name of the callable
            object, in the format "<fully qualified module name>:<fully
            qualified object name>". (e.g. "my.module:my_function")
        module_qualname (str): Qualified name of the module containing the
            callable object.
        object_qualname (str): Qualified name of the callable object within the
            module.
        path_to_module_dir (str): Path to the directory that contains the
            module that contains the callable object.
    """
    def __init__(
        self,
        fully_qualified_name: str,
        path_to_module_dir: str = os.getcwd()):
        """Initialize a LazyCallable object.

        Args:
            fully_qualified_name: Fully qualified name of the callable object,
                in the format "<fully qualified module name>:<fully qualified
                object name>". (e.g. "my.module:my_function")
            path_to_module_dir: Path to the directory that contains the module
                that contains the callable object.
        """
        self.fully_qualified_name = fully_qualified_name
        self.module_qualname, self.object_qualname = (
            fully_qualified_name.split(":"))
        self.module_qualname = self.module_qualname.replace(
            "/", ".").removesuffix(".py")
        self.path_to_module_dir = path_to_module_dir

        callable_object = self.get_callable()
        if callable_object.__class__.__name__ == "LLMChain":
            self.program_type = "LANGCHAIN"
        elif inspect.isfunction(callable_object):
            self.program_type = "FUNCTION"
        else:
            raise ValueError(
                f"Object {self.fully_qualified_name} is not a function or "
                "LangChain object.")

    def import_module(self) -> types.ModuleType:
        """Import the module containing the callable object.
        
        Returns:
            The imported module.
        """
        orig_sys_path = sys.path.copy()
        sys.path[0] = self.path_to_module_dir
        module = importlib.import_module(self.module_qualname)
        sys.path = orig_sys_path
        return module

    def get_callable(self) -> Callable:
        """Import the callable object and return it.
        
        Returns:
            Callable object.
        """
        try:
            module = importlib.import_module(self.module_qualname)
        except ModuleNotFoundError:
            module = self.import_module()
        callable_object = module
        for name in self.object_qualname.split("."):
            callable_object = getattr(callable_object, name)
        return callable_object

    def __call__(self, *args, **kwargs):
        """Call the callable object.
        
        Args:
            *args: Positional arguments to pass to the callable object.
            **kwargs: Keyword arguments to pass to the callable object.
        """
        callable_object = self.get_callable()
        if self.program_type == "LANGCHAIN":
            return callable_object.run(*args, **kwargs)
        else:
            return callable_object(*args, **kwargs)

    def get_parameter_keys(self) -> Iterable[str]:
        """Return the parameter names of the callable object.
        
        Returns:
            Iterable of the parameter names of the callable object.
        """
        callable_object = self.get_callable()
        if self.program_type == "LANGCHAIN":
            return callable_object.input_keys
        else:
            return inspect.signature(callable_object).parameters.keys()

    def get_inputs_signature(self) -> Dict[str, Optional[str]]:
        """Return the inputs signature of the callable object.
        
        Inputs signature is a map between input parameter names to
        strings indicating the corresponding parameter types (or to None for
        input parameters that do not have type annotations).
        """
        callable_object = self.get_callable()
        if self.program_type == "LANGCHAIN":
            return {key: None for key in callable_object.input_keys}
        else:
            signature = inspect.signature(callable_object)
            return {
                name: (
                    str(param.annotation)
                    if param.annotation != inspect._empty
                    else None)
                for name, param in signature.parameters.items()
            }


def get_test_suite_runs(
    local_vars: Dict[str, Any]) -> List[wire_model.CreateTestSuiteRunRequest]:
    """Return a list of test suite runs (which have not yet been executed).

    From the given dictionary, extract the relevant command line arguments,
    including the test suite file paths (which are required and contain
    additional configuration arguments). Create TestSuiteRun instances based on
    the specified hierarchy of configuration sources:
    1. Command line arguments.
    2. Test suite file arguments.
    3. Default arguments.
    In the case of a conflict, the lower-numbered item in the list takes
    precedence.
    
    Args:
        local_vars: Dictionary of local variables used to populate
            `wire_model.CreateTestSuiteRunRequest`. Only items with
            keys that are in `wire_model.CreateTestSuiteRunRequest`
            will be read.

    Returns:
        A list of `wire_model.CreateTestSuiteRunRequest` objects.

    Raises:
        ValueError: If the `test_suite_file_paths` argument is not defined in
            the given dictionary.
    """
    test_suite_file_paths = local_vars.get("test_suite_file_paths")
    if test_suite_file_paths is None:
        raise ValueError("test_suite_file_paths must be defined.")

    test_suite_runs = []
    for test_suite_file_path in test_suite_file_paths:
        # Process command line arguments and test suite file arguments
        # separately. Then merge them, with command line arguments taking
        # precedence.
        test_suite_cli_args = process_test_suite_args(local_vars)
        test_suite_file_args = _process_test_suite_file(
            test_suite_file_path, includes_config=True)
        test_suite_args = merge_test_suite_args(
            priority_1_dict=test_suite_cli_args,
            priority_2_dict=test_suite_file_args)

        # Process imports and merge them with the other arguments.
        for file in test_suite_args.get("imports", []):
            additional_args = _process_test_suite_file(
                file, includes_config=False)
            test_suite_args = merge_test_suite_args(
                priority_1_dict=test_suite_args,
                priority_2_dict=additional_args)

        # Create ProgramDetails object.
        callable_object = LazyCallable(
            test_suite_args.pop("llm_program_fully_qualified_name"))
        test_suite_args["llm_program_details"] = wire_model.ProgramDetails(
            fully_qualified_name=callable_object.fully_qualified_name,
            program_type=callable_object.program_type,
            inputs_signature=callable_object.get_inputs_signature())
        # TODO: The use-case for LazyCallable no longer exists. It should be
        # modified appropriately.

        # Test suite run has started.
        # TODO: This is not the right place to set this, but we need to set it
        # before we create the wire model object.
        test_suite_args["started_at"] = datetime.datetime.now(
            datetime.timezone.utc)

        test_suite_runs.append(
            wire_model.CreateTestSuiteRunRequest(**test_suite_args))

    return test_suite_runs


def merge_test_suite_args(
    priority_1_dict: Dict[str, Any],
    priority_2_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new dictionary by combining the contents of two dictionaries.

    The priority 1 dictionary takes precedence over the priority 2 dictionary.
    Values that are lists in both dictionaries are combined, not overwritten.
    
    Args:
        priority_1_dict: Dictionary that takes precedence over the priority 2
            dictionary.
        priority_2_dict: Dictionary that is overwritten by the priority 1
            dictionary.

    Returns:
        New dictionary that combines the contents of the two dictionaries.
    """
    merged_dict = copy.deepcopy(priority_2_dict)
    for key, value in priority_1_dict.items():
        # Combine values if both are lists.
        if (key in merged_dict and
            isinstance(merged_dict[key], list) and
            isinstance(value, list)):
            merged_dict[key].extend(value)
        # Otherwise update the value.
        else:
            merged_dict[key] = value
    return merged_dict


def process_test_suite_args(
    args: Dict[str, Any],
    ignore_invalid_args: bool = True) -> Dict[str, Any]:
    """Return a dictionary of test suite run arguments.

    Given a dictionary of arguments, return a new dictionary that contains
    only the arguments that correspond to
    `wire_model.CreateTestSuiteRunRequest` and whose values are not None or
    empty lists.

    Args:
        args: Dictionary of arguments to process.
        ignore_invalid_args: Whether to ignore arguments that do not correspond
            to `wire_model.CreateTestSuiteRunRequest`. If False, an exception
            will be raised if an argument does not correspond to the
            `wire_model.CreateTestSuiteRunRequest`.

    Returns:
        Dictionary of test suite arguments.

    Raises:
        ValueError: If `ignore_invalid_args` is False and an argument does
            not correspond to `wire_model.CreateTestSuiteRunRequest`.
    """
    processed_args = {}
    for key, value in args.items():
        if key in wire_model.CreateTestSuiteRunRequest.__annotations__:
            if (value is not None and
                not (isinstance(value, list) and len(value) == 0)):
                processed_args[key] = value
        elif key in ["id", "name", "description"]:
            processed_args[f"test_suite_{key}"] = value
        elif key == "imports":
            # TODO: Implement imports.
            raise NotImplementedError("Imports are coming soon!")
        elif key == "llm_program_fully_qualified_name":
            if value is not None:
                processed_args[key] = value
        elif not ignore_invalid_args:
            raise ValueError(f"Unknown argument: {key}")
    return processed_args


def _process_test_suite_file(
    path: Path,
    *,
    includes_config: bool) -> Dict[str, Any]:
    """Return a dictionary of test suite arguments from a test suite file.
    
    Read a test suite file and return a dictionary of arguments that correspond
    to `wire_model.CreateTestSuiteRunRequest`.

    Args:
        path: Path to the test suite file.
        includes_config: Whether the test suite file is expected to include a
            config entry.

    Returns:
        Dictionary of test suite arguments.

    Raises:
        ValueError: If the test suite file contains more than one config entry
            or if the test suite file does not contain a config entry and
            `includes_config` is True.
    """
    with open(path, "r") as f:
        yaml_content = yaml.safe_load(f)

    test_suite_file_args = {
        "test_cases": [],
        "quality_measures": [],
    }
    config_found = False

    for entry in yaml_content:
        for key, value in entry.items():

            if key in ["test", "test case", "test_case"]:
                inputs=value.get("inputs")
                output=value.get("output")
                description=value.get("description")
                if inputs is None:
                    inputs = value
                    if any((output, description)):
                        raise ValueError(
                            "If including output or description in a test "
                            "case, inputs must be defined in an explicit "
                            "inputs block.")
                test_suite_file_args["test_cases"].append(
                    wire_model.TestCase(
                        inputs=inputs,
                        output=output,
                        description=description))

            elif key in [
                "quality", "quality measure", "quality_measure", "measure"]:
                quality_measure = wire_model.QualityMeasure(**value)
                test_suite_file_args["quality_measures"].append(
                    quality_measure)

            elif key in ["hparam", "hparam spec", "hparam_spec"]:
                for k in ["name", "type"]:
                    value[f"hparam_{k}"] = value.pop(k)

                hparam_spec = wire_model.HparamSpec(**value)
                test_suite_file_args.setdefault("hparam_specs", []).append(
                    hparam_spec)

            elif key in ["config", "configuration"]:
                if includes_config and config_found:
                    raise ValueError(
                        "More than one config entry found in test suite file. "
                        "There must be exactly one config entry for each "
                        "test suite.")
                config_found = True
                if not includes_config:
                    raise ValueError(
                        "Only the primary test suite file may contain a "
                        "config entry.")
                config = process_test_suite_args(
                    value, ignore_invalid_args=False)
                test_suite_file_args.update(config)

            else:
                raise ValueError(f"Unknown entry: {key}")

    if not config_found and includes_config:
        raise ValueError(
            "No config entry found in test suite file. "
            "There must be exactly one config entry for each test suite.")
    return test_suite_file_args
