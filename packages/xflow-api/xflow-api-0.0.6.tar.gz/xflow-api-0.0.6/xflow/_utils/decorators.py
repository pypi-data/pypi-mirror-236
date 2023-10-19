import functools
import os


def client_method(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if os.getenv("SERVER_MODE") == "True":
            raise RuntimeError(f"client method: {func.__str__} can't be executed in server")
        return func(*args, **kwargs)
    return wrapper
