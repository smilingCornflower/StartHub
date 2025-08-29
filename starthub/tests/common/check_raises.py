from typing import Any


def check_raises_in_docs(func: Any, exc: type[Exception]) -> None:
    assert f":raises {exc.__name__}:" in func.__doc__
