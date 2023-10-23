import ast
import inspect
from dataclasses import fields
from typing import Any

from selfdocprint._layout_specs import (
    DEFAULT_STYLE,
    Layout,
    DefaultLayout,
    MinimalLayout,
    InlineLayout,
    DictLayout,
    ScrollLayout,
)
import selfdocprint._printer as printer
from selfdocprint._printer import sgr


_context_warning = f"{sgr('38:5:160')}Warning: selfdocprint not supported in this context.{sgr()}"


class PrintFunc:
    def __init__(self, default_layout: Layout = None):
        """Adds 'self-documenting' functionality to the built in print function.

        Args:
            default_layout (Layout, optional): Sets the default_layout used by __call__(). Defaults to None.
        """
        self.default_layout = default_layout
        self.show_context_warning = True

    def __call__(
        self,
        *values,
        layout: Layout = DefaultLayout,
        beg: str = "",
        end: str = "\n",
        sep: str = " ",
        file=None,
        flush: bool = False,
    ):
        """Prints the values to a stream, or to sys.stdout by default.
        If a layout is specified the arguments of the call to this function are
        turned into styled labels and printed in front of their values according
        to the specified layout. A single literal value or f-string is always
        printed without a label.

        Args:
            layout (Layout, optional): Layout to be used with the self-documenting functionality. Defaults to self.default_layout.
            beg (str, optional): string prepended in front of the output. Defaults to "".
            end (str, optional): string appended after the output. Defaults to "\n".
            sep (str, optional): string inserted between values. Defaults to " ". Ignored if a layout is set.
            file (_type_, optional): a file-like object (stream). Defaults to None.
            flush (bool, optional): whether to forcibly flush the stream. Defaults to False.
        """
        if layout == DefaultLayout:
            layout = self.default_layout

        if layout is None:  # do normal built-in print()
            print(*values, end=end, sep=sep, file=file, flush=flush)
            return

        try:
            call, _ = _get_call_info()
        except:
            # no source code available => do normal built-in print()
            if self.show_context_warning:
                print(_context_warning)
                self.show_context_warning = False
            print(*values, end=end, sep=sep, file=file, flush=flush)
            return

        arg_exprs = _getargument_expressions(call)

        if len(values) == 1 and _is_literal(
            arg_exprs[0]
        ):  # print single literals normally
            print(*values, end=end, sep=sep, file=file, flush=flush)
            return

        page = printer.press(arg_exprs, values, layout)
        print(beg, sep="", end="", file=file)
        print(
            page, sep="", end=end, file=file, flush=flush
        )  #  sep is ignored when a layout is used


def print_layout_specs():
    """Prints the specification for every built-in layout and a rudimentary
    description of the layout algoritm to the console.
    """
    # FIXME rethink and simplify this function
    sty = DEFAULT_STYLE + ";3"
    layouts = [
        InlineLayout(),
        DictLayout(),
        ScrollLayout(),
        MinimalLayout(),
    ]  # FIXME make this more efficient
    print()  # empty line at the start
    print("                   layout :  Inline     Dict       Scroll     Minimal")
    for fld in [
        field.name
        for field in fields(
            Layout,
        )
    ]:
        comment = ""
        label = None
        if fld == "literal_lbl":
            comment = "# used as a label for literal values"
        elif fld == "lbl_format":
            comment = "# applied to labels"
        elif fld == "int_format":
            comment = "# applied to values of type int"
        elif fld == "float_format":
            comment = "# applied to values of type float"
        elif fld == "str_format":
            comment = "# applied to all other value types after conversion to str"
        elif fld == "head":
            comment = "# printed at the beginning of the output"
        elif fld == "seperator":
            label = f"{sgr(sty)}{fld}{sgr()}.join([         "
            comment = "# printed inbetween the styled and formatted label/value pairs"
        elif fld == "style":
            label = f"    {sgr(sty)}{fld}{sgr()}(<label> +      "
            comment = "# style applied to the concatenation of <label> and pointer"
        elif fld == "pointer":
            label = f"    {sgr(sty)}{fld}{sgr()}) + <value>   "
            comment = "# printed in between the <label> and its associated <value>"
        elif fld == "tail":
            # print("    <value>")
            print("    , ...])")
            label = f"{sgr(sty)}{fld}{sgr()}                     "
            comment = "# printed at the end of the output"

        if label is None:
            label = f'{sgr(sty)}{format(fld, "<25")}{sgr()}'

        print(f"{label} :  ", end="")
        for l in layouts:
            val = getattr(l, fld)
            val = repr(val)
            print(format(val, "<11"), end="")
        print(comment)
    print()
    print(
        "# for the formatting specification see: https://docs.python.org/3/library/string.html#formatspec"
    )
    print(
        "# for the style code specification see: https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters"
    )
    print()  # empty line at the end


def _get_call_info(context: int = 2) -> (str, dict[str, Any]):
    """Returns the call to a function as source code plus the locals().
    With the default context it will return the info for the context
    from where the call to _get_call_info() was issued."""

    f_info = inspect.stack()[context]
    pos = f_info.positions
    if pos.lineno == pos.end_lineno:
        call = f_info.code_context[0][pos.col_offset : pos.end_col_offset]
    else:
        offset = f_info.frame.f_code.co_firstlineno
        source = inspect.getsource(f_info.frame)
        call = source.split("\n")[pos.lineno - offset : pos.end_lineno - offset + 1]
        call[0] = call[0][pos.col_offset :]
        call[-1] = call[-1][: pos.end_col_offset]
        call = "\n".join(call)
    return call, f_info.frame.f_locals


def _getargument_expressions(function_call: str) -> list[ast.expr]:
    """Parses function_call with the ast and returns the arguments of the call."""

    tree = ast.parse(function_call)
    # print(ast.dump(tree, indent=4))
    return tree.body[0].value.args


def _is_literal(arg_expr: ast.expr) -> bool:
    """Returns True if arg_expr is a literal."""

    return type(arg_expr) in [
        ast.Constant,
        ast.Dict,
        ast.JoinedStr,
        ast.List,
        ast.Set,
        ast.Tuple,
    ]
