from ultk.language.grammar import Grammar

family_grammar = Grammar.from_module("family.grammar_functions")


"""
From the above rules the following relations may be defined (Still need to test)
Mother: _ref_c(_m(O), S)
Mother: _ref_c(_f(O), S)
Son: _and(_or(_ref_c(_f(S), O), _ref_c(_m(s), O), _male(S))
Daughter: _and(_or(_ref_c(_f(S), O), _ref_c(_m(s), O), _female(S))
"""
