# Copyright 2023 Inductor, Inc.
"""Inductor client library."""

import contextlib
import contextvars
import copy
import datetime
import functools
import inspect
import io
import os
import sys
from typing import Any, Callable, Dict, Optional, TextIO, Tuple

from inductor import auth_session, backend_client, wire_model


# The following module-private variables are used by the functions in
# the rest of this module to transmit information to and from LLM program
# executions.
# Whether the logger decorator (inductor.logger) is enabled. This is set to
# False when running tests to prevent the logger from sending duplicate data to
# the backend, in the case that the LLM program being tested uses the logger
# decorator.
_logger_decorator_enabled = True
# Context variable used to store the logged values for the current LLM program
# execution. This is a context variable instead of a global variable so that
# the logger will work correctly when running mutliple threads that each use
# the logger decorator. However, an exception will be raised if the logger
# decorated function itself uses multiple threads that each call inductor.log.
_logged_values = contextvars.ContextVar("logged_values", default=None)
# Dictionary of hyperparameter values for the current LLM program execution.
_hparams = {}
# Context variable used to store whether the current LLM program execution is
# the primary execution.
_primary_execution = contextvars.ContextVar("active_execution", default=True)


def hparam(name: str, default_value: Any) -> Any:
    """Return the value of the hyperparameter having the given name.

    Args:
        name: Name of hyperparameter value to be returned.
        default_value: Value that will be returned if a value has not
            been specified for the given name.
    """
    return _hparams.get(name, default_value)


def _log(
    value: Any, *, after_complete: bool, description: Optional[str] = None):
    """Log a value and associate it with the current LLM program execution.

    Args:
        value: The value to be logged.
        after_complete: Whether the value was logged after the LLM
            program execution completed.
        description: An optional human-readable description of the logged
            value.
    
    Raises:
        RuntimeError: If the LLM program execution was not initiated via the
            Inductor CLI, and the LLM program is not decorated with
            @inductor.logger.
    """
    logged_values = _logged_values.get()
    if logged_values is None:
        # We can not distinguish between the below two cases described in the
        # exception message, so we raise the same exception in both cases.
        raise RuntimeError(
            "Cannot call inductor.log outside of a function decorated with "
            "@inductor.logger, unless you are running `inductor test`. "
            "Also note that invoking inductor.log from a thread different "
            "from the one that initialized the logger (via the decorator or "
            "the CLI tool) is currently unsupported. If you require support "
            "for this, please contact Inductor support to submit a feature "
            "request.")
    logged_values.append(
        wire_model.LoggedValue(
            value=copy.deepcopy(value),
            description=description,
            after_complete=after_complete))


def log(value: Any, *, description: Optional[str] = None):
    """Log a value and associate it with the current LLM program execution.

    Args:
        value: The value to be logged.
        description: An optional human-readable description of the logged
            value.
    
    Raises:
        RuntimeError: If the LLM program execution was not initiated via the
            Inductor CLI, and the LLM program is not decorated with
            @inductor.logger.
    """
    _log(value, description=description, after_complete=False)


@contextlib.contextmanager
def _configure_for_test(hparams: Dict[str, Any]):
    """Configure the Inductor library for a test suite run.
    
    Disable the inductor.logger decorator by setting
    `inductor._logger_decorator_enabled` to False and set the inductor._hparams
    to the given hyperparameters. On exit, restore the original value of
    `inductor._logger_decorator_enabled` and set `inductor._hparams` to an
    empty dictionary.

    Args:
        hparams: A dictionary mapping hyperparameter names to values.
    """
    global _hparams
    global _logger_decorator_enabled
    orig_logger_decorator_enabled = _logger_decorator_enabled
    try:
        _hparams = hparams
        _logger_decorator_enabled = False
        yield
    finally:
        _hparams = {}
        _logger_decorator_enabled = orig_logger_decorator_enabled


@contextlib.contextmanager
def _capture_logged_values():
    """Capture values logged via log() calls.
    
    If logging has not already been initialized, initialize logging by setting
    the logged values context variable (`_logged_values`) to an empty list,
    and, on exit, set `_logged_values` to `None`.
    If logging has already been initialized, do nothing.
    In either case, yield the list of logged values.

    The purpose of this context manager is to manage the state of the
    logged values context variable, which should only be initialized
    once per LLM program execution.

    Yields:
        The list of logged values.
    """
    logged_values = _logged_values.get()
    initializing_logged_values = logged_values is None
    try:
        if initializing_logged_values:
            _logged_values.set([])
        yield _logged_values.get()
    finally:
        if initializing_logged_values:
            _logged_values.set(None)


@contextlib.contextmanager
def _capture_stdout_stderr(
    suppress: bool = False) -> Tuple[io.StringIO, io.StringIO]:
    """Capture stdout and stderr.
    
    On exit, restore the original stdout and stderr and close the yielded
    StringIO buffers (i.e., the yielded buffers' contents will be discarded
    when context manager exits).
    
    Args:
        suppress: Whether to suppress stdout and stderr. If True, the
            contents of stdout and stderr will be suppressed after being
            captured. If False, stdout and stderr will behave as normal,
            but their contents will still be captured.

    Yields:
        A tuple of streams used to capture stdout and stderr.
    """
    class Tee(io.StringIO):
        """A StringIO buffer that optionally writes to a file in addition to
        capturing the written string."""
        def __init__(self, file: Optional[TextIO]):
            """Override the constructor to store the file to which to write."""
            self.file = file
            super().__init__()

        def write(self, s: str):
            """Override the write method to write to the file (as merited)
            in addition to capturing the written string."""
            if self.file is not None:
                self.file.write(s)
            return super().write(s)

    stdout_capture = Tee(
        sys.stdout if not suppress else None)
    stderr_capture = Tee(
        sys.stderr if not suppress else None)

    # Save the original stdout and stderr.
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    # Redirect stdout and stderr to the Tee objects.
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture
    try:
        yield (stdout_capture, stderr_capture)
    finally:
        # Restore the original stdout and stderr.
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        # Close the StringIO buffers.
        stdout_capture.close()
        stderr_capture.close()


def _get_module_qualname(f: Callable) -> str:
    """Return the fully qualified name of the module in which f is defined.

    Args:
        f: A function, class, or method.

    Returns:
        The fully qualified name of the module in which f is defined.  If f is
        defined in the __main__ module, then the name of the file containing f
        (without its ".py" extension) is returned as the fully qualified module
        name.

    Raises:
        RuntimeError if f is defined in the __main__ module and the name of the
        file containing f does not end with ".py".
    """
    qualname = f.__module__
    if qualname == "__main__":
        qualname, ext = os.path.splitext(
            os.path.basename(f.__globals__["__file__"]))
        if ext != ".py":
            raise RuntimeError(
                f"f ({f.__qualname__}) is defined in the __main__ module but "
                f"is contained in a file ({f.__globals__['__file__']}) that "
                "does not have extension '.py'.")
    return qualname


@contextlib.contextmanager
def _manage_executions():
    """Manage the state of the primary execution context variable.

    Manage the state of the primary execution context variable
    (_primary_execution). If the variable is initially True, it is set to
    False and True is yielded. If the variable is initially False, False is
    yielded. On exit, the variable is restored to its original value.

    The purpose of this context manager is to allow the logger decorator to
    determine whether it is the primary (top-level) execution. This is
    necessary because the logger decorator should only send data to the
    backend if it is the primary execution. For example, when the logger
    decorator decorates a function that is called by another function also
    decorated with the logger decorator, the logger decorator should not send
    data to the backend during the inner function call.

    Yields:
        True if the primary execution context variable was True, False
        otherwise.
    """
    primary_execution = _primary_execution.get()
    if primary_execution:
        _primary_execution.set(False)
    try:
        yield primary_execution
    finally:
        _primary_execution.set(primary_execution)


def logger(func: Callable) -> Callable:
    """Log the inputs, outputs, and inductor.log calls of func.

    Use `logger` as a decorator to automatically log the arguments and return
    value of, as well as calls to inductor.log within, the decorated function.
    For example:
        @inductor.logger
        def hello_world(name: str) -> str:
            inductor.log(len(name), description="name length")
            return f"Hello {name}!"

    Args:
        func: The decorated function.
    
    Returns:
        Wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if _logger_decorator_enabled:
            with (
                _capture_logged_values() as logged_values,
                _manage_executions() as primary_execution,
                # TODO: We don't need to capture stdout and stderr if we are
                # not in the primary execution. However since the stdout and
                # stderr are not suppressed, the user will not notice the
                # difference.
                _capture_stdout_stderr(suppress=False) as (stdout, stderr)
            ):
                auth_access_token = auth_session.get_auth_session().access_token

                llm_program_fully_qualified_name = (
                    f"{_get_module_qualname(func)}:{func.__qualname__}")

                # Get input arguments using the function's signature.
                signature = inspect.signature(func)
                bound_arguments = signature.bind(*args, **kwargs)
                bound_arguments.apply_defaults()
                input_args = copy.deepcopy(bound_arguments.arguments)

                # TODO: This code is duplicated in LazyCallable.
                inputs_signature = {
                    name: (
                        str(param.annotation)
                        if param.annotation != inspect._empty  # pylint: disable=protected-access
                        else None)
                    for name, param in signature.parameters.items()
                }

                started_at = datetime.datetime.now(datetime.timezone.utc)
                result = None
                error = None
                try:
                    result = func(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-except
                    error = str(e)
                output = copy.deepcopy(result)
                ended_at = datetime.datetime.now(datetime.timezone.utc)

                if primary_execution:
                    backend_client.log_llm_program_execution_request(
                        wire_model.LogLlmProgramExecutionRequest(
                            program_details=wire_model.ProgramDetails(
                                fully_qualified_name=
                                    llm_program_fully_qualified_name,
                                inputs_signature=inputs_signature,
                                program_type="FUNCTION"),
                            execution_details=wire_model.ExecutionDetails(
                                mode="DEPLOYED",
                                inputs=input_args,
                                hparams=_hparams or None,
                                output=output,
                                error=error,
                                stdout=stdout.getvalue(),
                                stderr=stderr.getvalue(),
                                logged_values=logged_values or None,
                                execution_time_secs=(
                                    ended_at - started_at).total_seconds(),
                                started_at=started_at,
                                ended_at=ended_at,)),
                        auth_access_token)

                else:
                    log(
                        {
                            "llm_program":
                            llm_program_fully_qualified_name,
                            "inputs": input_args,
                            "output": output
                        },
                        description="Nested LLM program execution")

                return result
        else:
            return func(*args, **kwargs)
    return wrapper
