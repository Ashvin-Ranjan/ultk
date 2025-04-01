from ultk.util.frozendict import FrozenDict
from ultk.util.io import write_expressions
from ultk.language.semantics import Meaning, Universe
from ultk.language.grammar import Grammar, GrammaticalExpression

from ..meaning import universe as kinship_universe
from ..grammar import kinship_grammar

def write_data(expressions_by_meaning: dict[Meaning, GrammaticalExpression]) -> None:
    # # For inspecting
    # fn = "kinship/outputs/expressions_and_extensions.txt"
    # results = {
    #     str(e): set(x for x in e.meaning if e.meaning[x])
    #     for e in expressions_by_meaning.values()
    # }
    # with open(fn, "w") as f:
    #     for k, v in results.items():
    #         f.write(k + "\n")
    #         f.write("-------------------------------------------\n")
    #         for x in v:
    #             f.write(str(x.name) + "\n")
    #         f.write("-------------------------------------------\n")

    # print(f"Wrote {len(expressions_by_meaning)} expressions to {fn}.")
    # For loading
    fn = "kinship/outputs/generated_expressions.txt"
    results: list[str] = [e.term_expression for e in expressions_by_meaning.values()]
    with open(fn, "w") as f:
        f.writelines(line + "\n" for line in sorted(results))

    print(f"Wrote {len(expressions_by_meaning)} expressions to {fn}.")



referents_index = {v.name: i for i, v in enumerate(kinship_universe.referents)}

max_len = 2 << len(kinship_universe.referents)

# This is to reduce the memory footprint of running at larger depths
def expr_key(expr: GrammaticalExpression):
    items = expr.evaluate(kinship_universe).mapping
    if type(next(iter(items.items()))[1]) == bool:
        out = 0
        for k, v in items.items():
            if v:
                out |= (2 << referents_index[k.name])
        return out
    else:
        out = hash(items[kinship_universe.referents[0]])
        return out

if __name__ == "__main__":

    expressions_by_meaning: dict[int, GrammaticalExpression] = (
        kinship_grammar.get_unique_expressions(
            4,  # I found 6 is too high
            max_size=2 ** len(kinship_universe),
            # max_size=100,
            unique_key=expr_key,
            compare_func=lambda e1, e2: len(e1) < len(e2),
        )
    )

    # filter out the trivial meaning, results in NaNs
    # iterate over keys, since we need to change the dict itself
    for meaning in list(expressions_by_meaning.keys()):
        if meaning == 0:
            del expressions_by_meaning[meaning]

    write_data(expressions_by_meaning)
