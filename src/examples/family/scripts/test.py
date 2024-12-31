from ..grammar import family_grammar
from ..meaning import universe

# This expression checks if they are the origin's mom
mother_expr = family_grammar.parse("_ref_c(_m(O), S)")
print("Mother:\n", mother_expr.evaluate(universe))

# This expression checks if they share the same parents and if the person is female
sister_expr = family_grammar.parse("_and(_and(_ref_c(_m(O), _m(S)), _ref_c(_f(O), _f(S))), _female(S))")
print("Sister:\n", sister_expr.evaluate(universe))