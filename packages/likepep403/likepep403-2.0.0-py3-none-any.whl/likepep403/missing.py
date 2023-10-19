class MissingType:
    """Class that provides the MISSING singleton."""

    __slots__ = ()
    __instance__ = None

    def __new__(cls):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
        return cls.__instance__

    def __repr__(self):
        return "<MISSING>"

    def __str__(self):
        return "MISSING"


MISSING = MissingType()


class MissingRequired(Exception):
    """No ``MISSING`` argument found."""
