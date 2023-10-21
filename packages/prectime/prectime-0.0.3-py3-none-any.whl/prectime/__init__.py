import io
import sys
import time
import logging
from types import FunctionType
from contextlib import contextmanager


DEFAULT_FORMAT = "{name} - {time}s\n"


class Measure(object):
    """
    A toolbox in which you can put a default output
    stream and change this stream for given methods.
    """
    def __init__(self, output: io.IOBase, round_digits: int, format: str=DEFAULT_FORMAT) -> None:
        self.output = output
        self.round_digits = round_digits
        self.format = format

    def _output_writeline(self, output, name, diff):
        output.write(self.format.format(name=name, time=round(diff, self.round_digits)))

    def _function(self, output):
        """
        A special method to mitigate the edge case of the Measure.function.
        """
        def wrapper(func):
            func = self.function(func, output)
            return func
        return wrapper

    def function(self, func_or_output=None, _output=None):
        """
        A decorator to measure the execution
        time of a function or method.
        """
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            diff = time.perf_counter() - start
            self._output_writeline(output, func.__name__, diff)
            return result
        if callable(func_or_output):
            func, output = func_or_output, (_output or self.output)
        elif isinstance(func_or_output, io.IOBase):
            return self._function(func_or_output)
        else:
            return self.function
        return wrapper

    @contextmanager
    def context(self, name=None, output=None):
        """
        Use this with a "with" expression.
        """
        if name is None:
            name = "measure.context"
        if output is None:
            output = self.output
        try:
            start = time.perf_counter()
            yield None
        finally:
            diff = time.perf_counter() - start
            self._output_writeline(output, name, diff)

    def _methods(self, ndigits):
        """
        A special method to mitigate the edge case of the Measure.function.
        """
        def wrapper(cls):
            cls = self.methods(cls, ndigits)
            return cls
        return wrapper

    def methods(self, cls_or_output=None, _output=None):
        """
        A method that decorates a class to wrap all methods 
        of this class in the Measure.function method.
        """
        if isinstance(cls_or_output, type):
            output = _output
        elif isinstance(cls_or_output, io.IOBase):
            return self._methods(cls_or_output)
        else:
            return self.methods
        cls = cls_or_output
        namespace = cls.__dict__
        for name, attr in namespace.items():
            if isinstance(attr, FunctionType):
                setattr(cls, name, self.function(attr, output))
        return cls


_measure = Measure(sys.stdout, 4)
function = _measure.function
context = _measure.context
methods = _measure.methods