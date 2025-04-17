import copy

from ultk.effcomm.optimization import EvolutionaryOptimizer
from ultk.util.io import read_grammatical_expressions, write_languages

from ..grammar import kinship_grammar
from ..meaning import universe as kinship_universe
from ultk.language.language import Language
from ..measures import comm_cost, complexity

from yaml import load
from tqdm import tqdm


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
        natural_languages = [Language(tuple(expressions_by_string[e] for e in l['lot_expressions']), name=l['name']) for l in load(f, Loader=Loader)]
    
    natural_languages = {language.name: language for language in natural_languages}

    target = [copy.copy(natural_languages["v_oldprussianprus1238"]) for _ in range(50)]

    explored_languages = []

    def lang_complexity(language):
        return complexity(language, expressions_by_meaning)

    optimizer = EvolutionaryOptimizer(
        [lang_complexity, comm_cost],
        expressions,
        2000,
        10,
        75,
    )

    for _ in tqdm(range(50)):
        # Keep track of visited
        explored_languages.extend(copy.copy(target))

        # Mutate dominating individuals
        target = optimizer.sample_mutated(target)

    # update with final generation
    explored_languages.extend(copy.copy(target))


    write_languages(
        list(set(explored_languages)),
        "kinship/outputs/random_drift.yml",
        {
            "name": lambda idx, _: f"drift-{idx}",
            "type": lambda _1, _2: "drift",
            "complexity": lambda _, lang: lang_complexity(lang),
            "comm_cost": lambda _, lang: comm_cost(lang),
        },
    )

    