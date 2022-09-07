from typing import Any


def satisfy(val: Any, req: Any) -> bool:
    if req is None:
        return True
    ans: bool
    try:
        ans = val.__satisfy__(req)
    except AttributeError:
        ans = (val == req)
    return ans


def inherent(child: Any, parent: Any) -> Any:
    if child is None:
        return parent
    ans: Any
    try:
        ans = child.__inherent__(parent)
    except AttributeError:
        ans = child
    return ans


class EnumError(Exception):
    pass


class NotMatched(Exception):
    val: Any
    req: Any


class PartError(Exception):
    pos: Any

