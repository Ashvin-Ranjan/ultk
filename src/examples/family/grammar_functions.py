from ultk.language.semantics import Referent
from .meaning import origin

# Basic Logical Operators
def _and(a: bool, b: bool) -> bool:
    return a and b

def _or(a: bool, b: bool) -> bool:
    return a or b

def _not(a: bool) -> bool:
    return not a

# Gender comparison
def _male(a: Referent) -> bool:
    if a is None:
        return False
    return a.gender == "m"

def _female(a: Referent) -> bool:
    if a is None:
        return False
    return a.gender == "f"

# Referent Comparison
def _ref_c(a: Referent, b: Referent) -> bool:
    if a is None or b is None:
        return False
    return a == b

# Getting mother and father of given referent
def _m(a: Referent) -> Referent:
    if a is None:
        return None
    return a.mother

def _f(a: Referent) -> Referent:
    if a is None:
        return None
    return a.father

# The self is the referent who is related to the origin
def Self(point: Referent, name: str = "S") -> Referent:
    return point

# The origin is who the referent is in relation with
def Origin(_: Referent, name: str = "O") -> Referent:
    return origin