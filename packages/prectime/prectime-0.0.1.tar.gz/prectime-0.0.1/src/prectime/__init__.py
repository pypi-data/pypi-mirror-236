import io
import sys
import time
from contextlib import contextmanager


class Measure(object):
    def __init__(self, output: io.IOBase=sys.stdout) -> None:
        self.output = output

    def _function(self, output):
        def wrapper(func):
            func = self.function(func, output)
            return func
        return wrapper

    def function(self, func_or_output=None, __output=None):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            diff = round(time.perf_counter() - start, 3)
            output.write(f"{func.__name__} - {diff}s\n")
            return result
        if callable(func_or_output):
            func, output = func_or_output, (__output if __output is not None else self.output)
        elif isinstance(func_or_output, io.IOBase):
            return self._function(func_or_output)
        else:
            return self.function
        return wrapper

    @contextmanager
    def context(self, name="measure.context", output=None):
        if output is None:
            output = self.output
        try:
            start = time.perf_counter()
            yield None
        finally:
            diff = round(time.perf_counter() - start, 3)
            output.write(f"{name} - {diff}s\n")


measure = Measure()
function = measure.function
context = measure.context