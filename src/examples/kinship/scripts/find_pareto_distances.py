from ultk.effcomm.tradeoff import non_dominated_2d, cdist
from ultk.util.io import read_grammatical_expressions

from ..grammar import kinship_grammar
from ..meaning import universe as kinship_universe

import numpy as np

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

    languages = []
    with open("kinship/data/langs_indian.txt", 'r') as f:
        language_names = f.read().split('\n')
    check_languages = {}

    max_cost = 0
    max_complexity = 0

    with open('kinship/outputs/natural_languages.yml', "r") as f:
        loaded = load(f, Loader=Loader)
        for l in loaded:
            if l['name'] in language_names:
                check_languages[l['name']] = (l["complexity"], l["comm_cost"])
            languages.append((l["complexity"], l["comm_cost"]))
            max_cost = max(max_cost, l['comm_cost'])
            max_complexity = max(max_complexity, l['complexity'])

    with open('kinship/outputs/explored_languages.yml', "r") as f:
        loaded = load(f, Loader=Loader)
        for l in loaded:
            languages.append((l["complexity"], l["comm_cost"]))
            max_cost = max(max_cost, l['comm_cost'])
            max_complexity = max(max_complexity, l['complexity'])
        
    dominating_indices = non_dominated_2d(
        tuple(languages)
    )
    dominating_languages = np.array(list(set([languages[idx] for idx in dominating_indices])))

    points = np.array(list(check_languages.values()))

    points[:, 0] = points[:, 0] / max_complexity
    dominating_languages[:, 0] = dominating_languages[:, 0] / max_complexity

    points[:, 1] = points[:, 1] / max_cost
    dominating_languages[:, 1] = dominating_languages[:, 1] / max_cost

    # Measure closeness of each language to any frontier point
    distances = cdist(points, dominating_languages)
    min_distances = np.min(distances, axis=1)

    # Normalize to 0, 1 because optimality is defined in terms of 1 - dist
    min_distances /= np.sqrt(2)

    for l, v in zip(check_languages.keys(), min_distances):
        print(f"Distance to Pareto frontier for {l}: {v}")

