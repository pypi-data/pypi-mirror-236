from dataclasses import dataclass

DEFAULT_STYLE: str = "95"


@dataclass
class Layout:
    """Defines a layout"""

    lbl_format: str = ""
    int_format: str = ""
    float_format: str = ""
    str_format: str = ""
    head: str = ""
    seperator: str = ""
    style: str = DEFAULT_STYLE
    pointer: str = ""
    tail: str = ""
    literal_lbl: str = "_"


@dataclass
class DefaultLayout(Layout):
    """Only used in the function declaration to indicate that by default
    the `layout` kwarg is set to self.default_layout."""

@dataclass
class MinimalLayout(Layout):
    """Prints a label in front of each value."""

    seperator: str = " "
    pointer: str = ":"
    tail: str = ""


@dataclass
class InlineLayout(Layout):
    """Prints a label in front of its value.
    Label/value pairs are printed from left to right.
    Multi-line value strings are properly aligned."""

    int_format: str = "-8"
    float_format: str = "-12.3f"
    str_format: str = "<"
    head: str = "\n"
    seperator: str = "   "
    pointer: str = ": "
    tail: str = ""


@dataclass
class DictLayout(Layout):
    """Prints a label in front of its value.
    Label/value pairs are printed from top to bottom.
    Multi-line value strings are properly aligned."""

    lbl_format: str = "<"
    int_format: str = "-8"
    float_format: str = "-12.3f"
    str_format: str = "<"
    head: str = "\n"
    seperator: str = "\n"
    pointer: str = " : "
    tail: str = ""


@dataclass
class ScrollLayout(Layout):
    """Prints a label above its value.
    Label/value pairs are printed from top to bottom."""

    head: str = "\n"
    seperator: str = "\n\n"
    pointer: str = ":\n"
    tail: str = "\n"
