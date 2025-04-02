from ultk.language.semantics import Referent, Universe
from .structure import domain
from ..data.prior_weights import weights

import numpy as np

sorted_names = sorted(domain)
sorted_weights = np.array([weights[name] for name in sorted_names])
prior = sorted_weights / (sorted_weights.sum()*2)

Ego = Referent("Ego")


male_prior = np.array((0,)*(len(sorted_names)) + tuple(sorted_weights / sorted_weights.sum()) + (0,))

female_prior = np.array(tuple(sorted_weights / sorted_weights.sum()) + (0,)*(len(sorted_names)+1))

female_referents = tuple(Referent(f"f{name}") for name in sorted_names)

male_referents = tuple(Referent(f"m{name}") for name in sorted_names)

universe = Universe(
    female_referents + male_referents + (Ego,),
    tuple(prior)*2 + (0,),
)

total_names = [f"m{name}" for name in sorted_names] + [f"f{name}" for name in sorted_names] + ["Ego"]