""" provides a decorator for fuzzing during testing """

from typing import Any, Callable
import afl # type: ignore

def afl_fuzz(f: Callable[..., Any]) -> Callable[..., Any]:
    """ decorator for fuzzing during testing """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """ fuzzes the decorated function """
        afl.init()
        afl.start()
        try:
            return f(*args, **kwargs)
        finally:
            afl.finish()
    return wrapper
