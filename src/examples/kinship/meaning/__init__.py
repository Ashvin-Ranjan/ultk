from ultk.language.semantics import Referent, Universe
from .structure import domain
from ..data.prior_weights import weights

import numpy as np

sorted_names = sorted(domain)
sorted_weights = np.array([weights[name] for name in sorted_names])
prior = sorted_weights / (sorted_weights.sum()*2)

Ego = Referent("Ego")

universe = Universe(
    tuple(Referent(f"f{name}") for name in sorted_names) + tuple(Referent(f"m{name}") for name in sorted_names) + (Ego,),
    tuple(prior)*2 + (0,),
)

total_names = [f"m{name}" for name in sorted_names] + [f"f{name}" for name in sorted_names] + ["Ego"]