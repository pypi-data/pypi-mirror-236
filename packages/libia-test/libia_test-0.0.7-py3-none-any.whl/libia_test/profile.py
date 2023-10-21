""" will be used to profile all functions in a module """

from importlib import import_module
from logging import getLogger, Logger
from types import ModuleType
from typing import Any
from line_profiler import LineProfiler

logger:Logger = getLogger(__name__)

def profile_module(module_name: str, functions: list[str]) -> None:
    """
    Profile the specified functions in the specified module.

    Args:
        module_name: The name of the module to wrap.
        functions: The names of the functions to profile.

    Raises:
        ImportError: If the module cannot be imported.
        AttributeError: If the specified functions do not exist in the module.
    """
    try:
        # Import the specified module dynamically
        module:ModuleType = import_module(module_name)
    except ImportError:
        logger.exception("Failed to import module: %s", module_name)
        raise

    # Create a LineProfiler object
    profiler:LineProfiler = LineProfiler()

    for function_name in functions:
        try:
            # Get the specified function from the module
            function:Any = getattr(module, function_name)
            profiler.add_function(function)
        except AttributeError:
            logger.warning(
                "%s does not exist in module: %s", function_name, module_name
            )

    # Run the main entry point of the module
    try:
        module.main()
    except Exception:
        logger.exception("An error occurred while running the module's main function")
        raise

    # Print the profiling statistics
    profiler.print_stats()
