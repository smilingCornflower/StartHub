from typing import Any, Callable


def check_raises(func: Callable[[Any], Any], exc: type[Exception]) -> None:
    assert f":raises {exc.__name__}:" in func.__doc__
