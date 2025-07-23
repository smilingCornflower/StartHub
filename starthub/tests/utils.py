from typing import Callable
from typing import Any

def check_raises(func: Callable[..., Any], exc: type[Exception]) -> None:
    assert func.__doc__ is not None and f":raises {exc.__name__}:" in func.__doc__
