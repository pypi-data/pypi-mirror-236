"""
Module with decorators allowing to set a block (a function or a class) as an
attribute of a function or class, or call another function with the block as an
argument.
"""

from collections.abc import Callable
from keyword import kwlist

from .abc import SupportsSetitem
from .missing import MISSING, MissingRequired

__all__ = ["setattr", "setitem", "call"]


_setattr = setattr


def setattr[R](obj: object, name: str | None = None):
    """
    Set the ``name`` attribute of ``obj`` to the decorated function or class.

    :param obj: The object to set the attribute of.
    :param name: The name of the attribute.
    :returns: The decorated function or class. This makes it easier to chain decorators.
    :raise AttributeError: ``name`` not in ``type(obj).__slots__``, or the object is immutable.
    :raise TypeError: The decorated object has no ``__name__`` and ``name`` is not a string.
    """

    def wrapper(value: R) -> R:
        if name is None and hasattr(value, "__name__") and value.__name__ not in kwlist:
            _setattr(obj, value.__name__, value)
        else:
            _setattr(obj, name, value)  # type: ignore
        return value

    return wrapper


def setitem[R](obj: SupportsSetitem, idx: object):
    """
    Set the ``idx`` item of ``obj`` to the decorated function or class.

    :param obj: The object to set the attribute of.
    :param idx: The item index to be set.
    :returns: The decorated function or class. This makes it easier to chain decorators.
    :raise TypeError: The object does not support subscript assignment.
    """

    def wrapper(value: R) -> R:
        obj[idx] = value
        return value

    return wrapper


def call[
    R
](fn: Callable[..., R], /, *args: object, **kwargs: object) -> Callable[[Callable], R]:
    """
    Call ``fn`` with ``args`` and ``kwargs``, substituting each ``MISSING``
    definition with the decorated function.

    :param fn: The object to set the attribute of.
    :param args: The positional arguments to call ``fn`` with. Either it or ``kwargs`` must have a ``MISSING`` argument.
    :param kwargs: The keyword arguments to call ``fn`` with. Either it or ``args`` must have a ``MISSING`` argument.
    :returns: The decorated function or class. This makes it easier to chain decorators.
    :raise TypeError: ``fn`` is not callable.
    :raise MissingRequired: There is no ``MISSING`` argument in either ``args`` or ``kwargs``.
    """

    def wrapper(_: Callable) -> R:
        a = list(args)
        if MISSING not in a + list(kwargs.values()):
            raise MissingRequired(
                "Must have at least one <MISSING> argument, found none"
            )
        for i, v in enumerate(a):
            if v is MISSING:
                a[i] = _
        for k, v in kwargs.items():
            if v is MISSING:
                kwargs[k] = v
        return fn(*a, **kwargs)

    return wrapper
