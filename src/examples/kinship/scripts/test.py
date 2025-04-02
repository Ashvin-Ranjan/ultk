from ultk.language.grammar.grammar import GrammaticalExpression
from ultk.language.language import Language
from ultk.language.semantics import Meaning

from ..meaning import universe, male_prior
from ..grammar import kinship_grammar
from ..measures import comm_cost, complexity

from ..data.prior_weights import weights


def write_data(expressions_by_meaning: list[Meaning, GrammaticalExpression]) -> None:
    # For inspecting
    fn = "kinship/outputs/test_expressions_and_extensions.txt"
    results = {
        str(e): set(x for x in e.meaning if e.meaning[x])
        for e in expressions_by_meaning.values()
    }
    with open(fn, "w") as f:
        for k, v in results.items():
            f.write(k + "\n")
            f.write("-------------------------------------------\n")
            for x in v:
                f.write(str(x.name) + "\n")
            f.write("-------------------------------------------\n")

    print(f"Wrote {len(expressions_by_meaning)} expressions to {fn}.")

exprs = {}

with open("kinship/outputs/test_expressions.txt", 'r') as f:
    for i in f.read().split('\n'):
        expr = kinship_grammar.parse(i)
        exprs[expr.evaluate(universe)] = expr

write_data(exprs)

lang = Language(tuple(exprs.values()), name="test", natural=False)

print(comm_cost(lang))