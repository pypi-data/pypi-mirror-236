from collections.abc import Callable

from .missing import MISSING


class Caller:
    def __init__(self, fn, /, *args, **kwargs):
        self.fn = fn
        self.args = list(args)
        self.kwargs = kwargs

    def register(self, idx: str | int | tuple[()] = (), item: object = MISSING, /) -> Callable | None:  # type: ignore
        def wrap(i):
            match idx:
                case int() | ():
                    if idx in (len(self.args), ()):
                        self.args.append(i)
                    else:
                        self.args[idx] = i
                case str():
                    self.kwargs[idx] = i
                case tuple():
                    raise TypeError(
                        f"Expected type of index to be int, str, or an empty tuple, got a non-empty tuple"
                    )
                case _:
                    raise TypeError(
                        f"Expected type of index to be int, str, or (), got {type(idx).__qualname__!r}"
                    )
            return i

        if item is MISSING:
            return wrap
        wrap(item)

    def __call__(self):
        return self.fn(*self.args, **self.kwargs)

    call = exec = __call__
