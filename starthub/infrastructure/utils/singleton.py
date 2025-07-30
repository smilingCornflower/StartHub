import threading
from functools import wraps
from typing import Any, Callable


def singleton[T](cls: type[T]) -> Callable[..., T]:
    instances = {}
    lock = threading.Lock()

    @wraps(cls)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
