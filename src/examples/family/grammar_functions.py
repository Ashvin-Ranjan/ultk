from typing import Any
from ultk.language.semantics import Referent
from ultk.util.frozendict import FrozenDict
from .meaning import origin

start = bool

# Basic Logical Operators
def _and(a: bool, b: bool) -> bool:
    return a and b

def _or(a: bool, b: bool) -> bool:
    return a or b

def _not(a: bool) -> bool:
    return not a

# Gender comparison
def _male(a: FrozenDict[str, Any]) -> bool:
    if a is None:
        return False
    return a["gender"] == "m"

def _female(a: FrozenDict[str, Any]) -> bool:
    if a is None:
        return False
    return a["gender"] == "f"

# Referent Comparison
def _ref_c(a: FrozenDict[str, Any], b: FrozenDict[str, Any]) -> bool:
    if a is None or b is None:
        return False
    return a == b

# Getting mother and father of given referent
def _m(a: FrozenDict[str, Any]) -> FrozenDict[str, Any]:
    if a is None or a["mother"] is None:
        return None
    return FrozenDict(a["mother"].__dict__)

def _f(a: FrozenDict[str, Any]) -> FrozenDict[str, Any]:
    if a is None or a["father"] is None:
        return None
    return FrozenDict(a["father"].__dict__)

# The self is the referent who is related to the origin
def Self(point: Referent, name: str = "S") -> FrozenDict[str, Any]:
    return FrozenDict(point.__dict__)

# The origin is who the referent is in relation with
def Origin(_: Referent, name: str = "O") -> FrozenDict[str, Any]:
    return FrozenDict(origin.__dict__)