from ultk.effcomm.optimization import EvolutionaryOptimizer
from ultk.language.sampling import random_languages
from ultk.util.io import read_grammatical_expressions


from ..grammar import family_grammar
from ..meaning import universe as family_universe
from ..measures import comm_cost, complexity
from ..util import write_languages

if __name__ == "__main__":
    expressions, expressions_by_meaning = read_grammatical_expressions(
        "family/outputs/generated_expressions.yml",
        family_grammar,
        universe=family_universe,
        return_by_meaning=True,
    )

    seed_languages = random_languages(
        expressions, sampling_strategy="stratified", sample_size=1000, max_size=10
    )

    def lang_complexity(language):
        return complexity(language, expressions_by_meaning)

    optimizer = EvolutionaryOptimizer(
        [lang_complexity, comm_cost],
        expressions,
        1000,
        3,
        50,
    )
    result = optimizer.fit(seed_languages)

    write_languages(
        result["dominating_languages"],
        "family/outputs/dominating_languages.yml",
        {
            "name": lambda idx, _: f"dominating-{idx}",
            "type": lambda _1, _2: "dominant",
            "complexity": lambda _, lang: lang_complexity(lang),
            "comm_cost": lambda _, lang: comm_cost(lang),
        },
    )
    write_languages(
        result["explored_languages"],
        "family/outputs/explored_languages.yml",
        {
            "name": lambda idx, _: f"explored-{idx}",
            "type": lambda _1, _2: "explored",
            "complexity": lambda _, lang: lang_complexity(lang),
            "comm_cost": lambda _, lang: comm_cost(lang),
        },
    )
