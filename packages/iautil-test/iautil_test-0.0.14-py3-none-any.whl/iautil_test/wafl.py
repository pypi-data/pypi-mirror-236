""" provides a decorator for fuzzing during testing """

from functools import wraps
#from typing import Any
from typing import Callable, ParamSpec, TypeVar
import afl

T = TypeVar('T')
P = ParamSpec('P')

def afl_fuzz(f: Callable[P, T]) -> Callable[P, T]:
    """ decorator for fuzzing during testing """
    @wraps(f)
    def wrapper(*args:P.args, **kwargs:P.kwargs) -> T:
        """ fuzzes the decorated function """
        afl.init()
        afl.start()
        try:
            return f(*args, **kwargs)
        finally:
            afl.finish()
    return wrapper
