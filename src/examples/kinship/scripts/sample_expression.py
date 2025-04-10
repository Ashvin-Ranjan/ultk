from math import log
import ultk.language.grammar.inference
from ultk.language.grammar.likelihood import all_or_nothing, noise_match, percent_match
from ..grammar import kinship_grammar
from ..meaning import universe as kinship_universe

refs = ['fF', 'fFeB', 'fFyB', 'mF', 'mFeB', 'mFyB']

# mD, meBD, myBD
# *(my_(axy_and_by(axy_or_bxy(axy_and_bx(child, female), Ez_axz_and_bzy(axy_and_bx(child, female), axy_and_bx(sibling, male))), male)), .)

data = [(ref, ref.name in refs) for ref in kinship_universe.referents]

def log_safe(x):
    try:
        return log(x)
    except:
        return float('-inf')

exp = kinship_grammar.generate(kinship_grammar._start)

probability_func = noise_match(2)

print("Loaded",exp, f"({probability_func(data, exp)})")

while percent_match(data, exp) != 1:
    prevl = len(exp)
    # Sample a new expression
    exp = ultk.language.grammar.inference.log_mh_sample(
            exp,
            kinship_grammar,
            data,
            probability_func,
        )

    print(f"---\n`{exp}` ({probability_func(data, exp)}, {percent_match(data, exp)})")

print("---\nSOLUTION FOUND")