import ast
import io
import re
from contextlib import closing
from typing import Callable
from ._layout_specs import Layout


class _Pane:
    """Holds a formatted and layed-out label/value pair."""

    def __init__(self, layout: Layout, label: str, value: object, max_lbl_width: int):
        """Formats and lays out the label and its value."""
        self.layout = layout
        lbl_format = _fixate_alignment_width(layout.lbl_format, max_lbl_width)
        label = f"{sgr(layout.style)}{format(label, lbl_format)}{layout.pointer}{sgr()}"
        col_ofs = self._update_col_offset(_strip_styles(label))
        if isinstance(value, bool):
            val_str = format(str(value), layout.str_format)
        elif isinstance(value, int):
            val_str = format(value, layout.int_format)
        elif isinstance(value, float):
            val_str = format(value, layout.float_format)
        else:
            value_lines = str(value).split("\n")
            max_value_line_len = max(len(vl) for vl in value_lines)
            value_format = _fixate_alignment_width(
                layout.str_format, max_value_line_len
            )
            value_lines = [format(l, value_format) for l in value_lines]
            if _has_alignment(layout):
                val_str = ("\n" + " " * col_ofs).join(value_lines)
            else:
                val_str = ("\n").join(value_lines)
        self.lines = (label + val_str).split("\n")
        self.line_max_len = max(len(_strip_styles(l)) for l in self.lines)
        self.line_count: int = len(self.lines)

    def __str__(self):
        return "\n".join(self.lines)

    def get_line(self, i: int):
        if i < self.line_count:
            return self.lines[i]
        else:
            if _has_alignment(self.layout):
                return " " * self.line_max_len
            else:
                return ""

    def _update_col_offset(self, s: str, start_col_ofs: int = 0) -> int:
        """Calculates the new column offset if s were printed starting at start_col_ofs."""
        l = len(s)
        if (col_ofs := s.rfind("\n")) > -1:
            return l - col_ofs - 1
        else:
            return start_col_ofs + l


def press(args: list[ast.expr], values: list[object], layout: Layout) -> str:
    labels = [_create_label(arg, layout.literal_lbl) for arg in args]
    max_lbl_width: int = _getlongest_line_len(labels)
    panes = [
        _Pane(layout, lbl, val, max_lbl_width) for (lbl, val) in zip(labels, values)
    ]
    with closing(io.StringIO("")) as buf:
        if _isleft_to_right_layout(layout) and _has_alignment(layout):
            max_lines = max([pane.line_count for pane in panes])
            beg, pre, post, end = _get_edges(layout.head, layout.tail)
            buf.write(beg)
            for l in range(max_lines):
                buf.write(pre)
                buf.write(layout.seperator.join(pane.get_line(l) for pane in panes))
                buf.write(post)
                if l < max_lines - 1:
                    buf.write("\n")
            # buf.write(end)
        else:
            buf.write(layout.head)
            buf.write(layout.seperator.join(str(pane) for pane in panes))
            buf.write(layout.tail)
        return buf.getvalue()


def format_objects(
    objects: list[any], int_format, float_format, str_format
) -> (list[list[str]], int):
    result_list = []
    max_width = 0
    for value in objects:
        if isinstance(value, bool):
            result_list.append(list(format(str(value), str_format)))
        elif isinstance(value, int):
            result_list.append(list(format(str(value), int_format)))
        elif isinstance(value, float):
            result_list.append(list(format(str(value), float_format)))
        else:
            value_lines = str(value).split("\n")
            max_value_line_len = max(len(vl) for vl in value_lines)
            value_format = _fixate_alignment_width(str_format, max_value_line_len)
            value_lines = [format(l, value_format) for l in value_lines]
            # if _has_alignment(layout):
            #     val_str = ("\n" + " " * col_ofs).join(value_lines)
            # else:
            #     val_str = ("\n").join(value_lines)
    return (result_list, max_width)


def iswithin_max_width(page: str, max_width) -> bool:
    page = _strip_styles(page)
    if _getlongest_line_len([page]) < max_width:
        return True
    return False


def sgr(sgr_codes: str = None):
    if sgr_codes is None:
        sgr_codes = "0"
    return f"\033[{sgr_codes}m"


def _has_alignment(layout: Layout):
    return re.match(r".*[<>^].*", layout.str_format) is not None


def _isleft_to_right_layout(layout: Layout) -> bool:
    for attr in {"seperator", "pointer"}:
        # for attr in {"sep"}: # for next version with flexible tables
        if "\n" in getattr(layout, attr):
            return False
    return True


def _get_edges(beg: str, end: str):
    if (last_nl := beg.rfind("\n")) != -1:
        pre = beg[last_nl + 1 :]
        beg = beg[: last_nl + 1]
    else:
        pre = beg

    if (first_nl := end.find("\n")) != -1:
        post = end[: first_nl + 1]
        end = end[first_nl + 1 :]
    else:
        post = end

    return beg, pre, post, end


def _fixate_alignment_width(format_spec: str, fixed_width: int):
    """Checks for an 'align' char in format_spec and appends fixed_width if the
    width for the alignment is not specified"""

    # The following pattern captures an align specification without a width: an align character,
    # followed by zero or more '0' chars (specified inside an Atomic group), but not followed by a digit.
    pattern = r"([<>^](?>0*))(?![1-9])"
    return re.sub(
        pattern,
        r"\g<1>" + str(fixed_width),
        format_spec,
        count=1,
    )


def _getlongest_line_len(strs: list[str]) -> int:
    """check each line in each string in strs and return the longest line"""
    longest_lines = [max(s.split("\n"), key=len) for s in strs]
    if len(longest_lines) == 0:
        return 0
    else:
        return len(max(longest_lines, key=len))


def _strip_styles(s: str) -> str:
    """returns s with style codes removed"""
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    result = ansi_escape.sub("", s)
    return result


def _create_label(arg: ast.expr, literal_str: str):
    # for info on ast types: https://greentreesnakes.readthedocs.io/en/latest/nodes.html
    DEPRECATED_STR = f"Unexpected argument: {ast.unparse(arg)} (ast type is deprecated)"
    NOT_POSSIBLE_STR = f"Unexpected argument: {ast.unparse(arg)} (shouldn't be possible as arg in print() )"
    UNSUPPORTED = f"Unsupported argument: {ast.unparse(arg)}"
    # print(type(arg))
    for arg_type, action in [
        (ast.Attribute, ast.unparse),
        (ast.Await, UNSUPPORTED),
        (ast.BinOp, ast.unparse),
        (ast.BoolOp, ast.unparse),
        (ast.Bytes, DEPRECATED_STR),
        (ast.Call, ast.unparse),
        (ast.Compare, ast.unparse),
        (ast.Constant, lambda x: literal_str),
        (ast.Dict, lambda x: literal_str),
        (ast.DictComp, ast.unparse),
        (ast.Ellipsis, DEPRECATED_STR),
        (ast.FormattedValue, NOT_POSSIBLE_STR),
        (ast.GeneratorExp, ast.unparse),
        (ast.IfExp, ast.unparse),
        (ast.JoinedStr, lambda x: literal_str),
        (ast.Lambda, ast.unparse),
        (ast.List, lambda x: literal_str),
        (ast.ListComp, ast.unparse),
        (ast.Name, ast.unparse),
        (ast.NameConstant, DEPRECATED_STR),
        (ast.NamedExpr, ast.unparse),
        (ast.Num, DEPRECATED_STR),
        (ast.Set, lambda x: literal_str),
        (ast.SetComp, ast.unparse),
        (ast.Slice, NOT_POSSIBLE_STR),
        (ast.Starred, UNSUPPORTED),
        (ast.Str, DEPRECATED_STR),
        (ast.Subscript, ast.unparse),
        (ast.Tuple, lambda x: literal_str),
        (ast.UnaryOp, ast.unparse),
        (ast.Yield, UNSUPPORTED),
        (ast.YieldFrom, UNSUPPORTED),
    ]:
        if isinstance(arg, arg_type):
            if isinstance(action, Callable):
                return action(arg)
            else:
                raise ValueError(action)
    return f"unknow arg encoutered: {arg}"
