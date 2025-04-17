from ultk.effcomm.optimization import EvolutionaryOptimizer
from ultk.language.sampling import random_languages
from ultk.util.io import read_grammatical_expressions, write_expressions

from ..grammar import kinship_grammar
from ..meaning import universe as kinship_universe
from ..measures import comm_cost, complexity
from ultk.util.io import write_languages
from ultk.language.language import Language

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


if __name__ == "__main__":
    expressions, expressions_by_meaning = read_grammatical_expressions(
        "kinship/outputs/generated_expressions.yaml",
        kinship_grammar,
        universe=kinship_universe,
        return_by_meaning=True,
    )

    expressions_by_string = {str(e): e for e in expressions}

    with open('kinship/outputs/natural_languages.yml', "r") as f:
        natural_languages = [Language(tuple(expressions_by_string[e] for e in l['lot_expressions'])) for l in load(f, Loader=Loader)]
    
    seed_languages = random_languages(
        expressions, sampling_strategy="stratified", sample_size=1000, max_size=10
    ) + natural_languages

    def lang_complexity(language):
        return complexity(language, expressions_by_meaning)

    optimizer = EvolutionaryOptimizer(
        [lang_complexity, comm_cost],
        expressions,
        1000,
        10,
        50,
    )
    result = optimizer.fit(seed_languages)

    write_languages(
        result["dominating_languages"],
        "kinship/outputs/dominating_languages.yml",
        {
            "name": lambda idx, _: f"dominating-{idx}",
            "type": lambda _1, _2: "dominant",
            "complexity": lambda _, lang: lang_complexity(lang),
            "comm_cost": lambda _, lang: comm_cost(lang),
        },
    )
    write_languages(
        result["explored_languages"],
        "kinship/outputs/explored_languages.yml",
        {
            "name": lambda idx, _: f"explored-{idx}",
            "type": lambda _1, _2: "explored",
            "complexity": lambda _, lang: lang_complexity(lang),
            "comm_cost": lambda _, lang: comm_cost(lang),
        },
    )
