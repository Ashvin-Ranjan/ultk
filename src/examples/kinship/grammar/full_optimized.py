"""Smaller kinship grammar."""

from ultk.language.semantics import Referent
from examples.kinship.meaning.structure import kinship_structure
from examples.kinship.meaning import Ego, universe

from typing import NewType, Any


# t = bool
# e = Referent
# et = Callable[[e], t]
# eet = Callable[[e], et]
# arg = tuple[e]

# start = t

t = bool
# Referent
e = Referent
arg = NewType("arg", Referent)

# The first argument is the ID of the function, the second is the ID of the referent 
et = NewType("et", tuple[int, tuple[Any, ...]]) 
eet = NewType("eet", tuple[int, tuple[Any, ...]])

start = t

##############################################################################
# Conversion from tuple data to actual function calls
##############################################################################

# The reason this is needed is because labmdas mess everything up
# - They take up way too much memory at higher depths
# - They cannot be saved to YAML files
# As such the structure is to be instead tuples containing the ID of the function and the ID of the arguments
# This saves on memory and can be stored nicely!!

def closure(x, y, a, visited=None):
    # Track visited nodes to avoid infinite loops
    if visited is None:
        visited = set()
    if (x, y) in visited:
        return False
    visited.add((x, y))

    # Base case: direct relationship exists
    if eet_function_map[a[0]](x, *a[1])(y):
        return True

    # Recursive case: check for intermediary z
    return any(eet_function_map[a[0]](x, *a[1])(z) and closure(z, y, a, visited) for z in universe if z != x)

def sibling_predicate(x, y):
    # x and y must share at least one parent
    shared_parent = any(
        kinship_structure.evaluate("is_parent", z.name, x.name)
        and kinship_structure.evaluate("is_parent", z.name, y.name)
        for z in universe
    )
    # Exclude self
    return shared_parent and x != y

et_function_map = [
    # male
    lambda x, ref: kinship_structure.evaluate("is_male", x.name, ref.name),
    # female
    lambda x, ref: not kinship_structure.evaluate("is_male", x.name, ref.name),
    # my_
    lambda x, a: x != Ego and eet_function_map[a[0]](x, *a[1])(Ego), # TODO: Update to collapse a instead of treating as function
]

eet_function_map = [
    # parent
    lambda x: lambda y: kinship_structure.evaluate("is_parent", x.name, y.name),
    # child
    lambda x: lambda y: kinship_structure.evaluate("is_parent", y.name, x.name),
    # older
    lambda x: lambda y: kinship_structure.evaluate("is_older", x.name, y.name),
    # younger
    lambda x: lambda y: kinship_structure.evaluate("is_older", y.name, x.name),
    # same_sex
    lambda x, ref: lambda y: kinship_structure.evaluate("is_male", x.name, ref.name) == kinship_structure.evaluate("is_male", y.name, ref.name),
    # diff_sex
    lambda x, ref: lambda y: kinship_structure.evaluate("is_male", x.name, ref.name) != kinship_structure.evaluate("is_male", y.name, ref.name),
    # axy_and_by
    lambda x, a, b: lambda y: eet_function_map[a[0]](x, *a[1])(y) and et_function_map[b[0]](y, *b[1]),
    # axy_and_bx
    lambda x, a, b: lambda y: eet_function_map[a[0]](x, *a[1])(y) and et_function_map[b[0]](x, *b[1]),
    # axy_and_bxy
    lambda x, a, b: lambda y: eet_function_map[a[0]](x, *a[1])(y) and eet_function_map[b[0]](x, *b[1])(y),
    # axy_or_by
    lambda x, a, b: lambda y: eet_function_map[a[0]](x, *a[1])(y) or et_function_map[b[0]](y, *b[1]),
    # axy_or_bx
    lambda x, a, b: lambda y: eet_function_map[a[0]](x, *a[1])(y) or et_function_map[b[0]](x, *b[1]),
    # axy_or_bxy
    lambda x, a, b: lambda y: eet_function_map[a[0]](x, *a[1])(y) or eet_function_map[b[0]](x, *b[1])(y),
    # Ez_axz_and_bzy
    lambda x, a, b: lambda y: any(z for z in universe if eet_function_map[a[0]](x, *a[1])(z) and eet_function_map[b[0]](z, *b[1])(y)),
    # inv
    lambda x, a: lambda y: eet_function_map[a[0]](y, *a[1])(x),
    # <->
    lambda x, a: lambda y: eet_function_map[a[0]](x, *a[1])(y) or eet_function_map[a[0]](y, *a[1])(x),
    # tr_cl
    lambda x, a: lambda y: closure(x, y, a),
    # siblings
    lambda x: lambda y: sibling_predicate(x, y),
]



##############################################################################
# Bind/Apply logic
##############################################################################


# Then unwrap args and apply predicate
# t -> et arg
def apply_et(p: et, a: arg, name="*") -> t:
    return et_function_map[p[0]](a, *p[1])


# Exclude this to require only ego_relative expressions are grammatical
# # et -> eet arg
# def apply_eet(p: eet, a: arg, name="**") -> et:
#     return p(*a)


# Need to bind args for intermediate node
# arg -> Referent ...
def bind(a: Referent, name=".") -> arg:
    return a


##############################################################################
# Terminal rules
##############################################################################


# Using dummy args because grammar rules aren't considered terminal unless they take Referents
# et -> e
# ID: 0
def male(ref: e) -> et:
    return (0, (ref,))


# et -> e
# ID: 1
def female(ref: e) -> et:
    return (1, (ref,))


# eet -> e
# ID: 0
def parent(*_: e) -> eet:
    return (0, tuple())


# eet -> e
# ID: 1
def child(*_: e) -> eet:
    return (1, tuple())


# eet -> e
# ID: 2
def older(*_: e) -> eet:
    return (2, tuple())


# eet -> e
# ID: 3
def younger(*_: e) -> eet:
    return (3, tuple())


# eet -> e
# ID: 4
def same_sex(ref: e) -> eet:
    return (4, (ref,))

# eet -> e
# ID: 5
def diff_sex(ref: e) -> eet:
    return (5, (ref,))

##############################################################################
# Nonterminal rules
##############################################################################


# The 'ego_relative' predicate. Use an exclusive version.
# To get inclusive, in case you want things like 'parent of my child',
# use lambda _: a(_)(Ego)
# et -> eet
# ID: 2
def my_exclusive(a: eet, name="my_") -> et:
    return (2, (a,))


# et -> eet et
# ID: 6
def axy_and_by(a: eet, b: et) -> eet:
    return (6, (a, b))


# et -> eet et
# ID: 7
def axy_and_bx(a: eet, b: et) -> eet:
    return (7, (a, b))


# eet -> eet eet
# ID: 8
def axy_and_bxy(a: eet, b: eet) -> eet:
    return (8, (a, b))


# et -> eet et
# ID: 9
def axy_or_by(a: eet, b: et) -> eet:
    return (9, (a, b))


# et -> eet et
# ID: 10
def axy_or_bx(a: eet, b: et) -> eet:
    return (10, (a, b))


# eet -> eet eet
# ID: 11
def axy_or_bxy(a: eet, b: eet) -> eet:
    return (11, (a, b))


# ∃z( A(x,z) ^ B(z, y) )
# eet -> eet eet
# ID: 12
def Ez_axz_and_bzy(a: eet, b: eet) -> eet:
    return (12, (a, b))


# eet -> eet
# ID: 13
def inv(a: eet, name="inv") -> eet:
    return (13, (a,))


# eet -> eet
# ID: 14
def sym(a: eet, name="<->") -> eet:
    return (14, (a,))


# transitive closure, e.g. 'ancestor-of'
# eet -> eet
# ID: 15
def tr_cl(a: eet) -> eet:
    return (15, (a,))


# Technically the KR2012 definition of aunt/uncle includes Mother and Father...
# eet -> e
# ID: 16
def exclusive_sibling(*_: e, name="sibling") -> eet:
    return (16, ())

grammar_rules = (
    apply_et,
    bind,
    male,
    female,
    parent,
    child,
    older,
    younger,
    same_sex,
    diff_sex,
    my_exclusive,
    axy_and_by,
    axy_and_bx,
    axy_and_bxy,
    axy_or_by,
    axy_or_bx,
    axy_or_bxy,
    Ez_axz_and_bzy,
    inv,
    sym,
    tr_cl,
    exclusive_sibling,
)