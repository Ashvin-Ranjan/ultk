import pandas as pd
from ultk.language.semantics import Universe, Referent

# This generates referents whose attributes are themselves the referents of their mother and father

def generate_referents(target, referents_dict, referents_linked):
    # The current referent to add
    val = referents_dict[target]

    # Base case (If there is no known mom or dad then just add them straight to the dictionary)
    if val["mother"] == "unk" and val["father"] == "unk":
        return {
            target: Referent(target, {"mother": None, "father": None, "gender": val["gender"]})
        }
    
    # Some setup data
    out = {}
    ref_data = {
        "mother": None,
        "father": None,
        "gender": val["gender"]
    }

    # Add the mother
    if val["mother"] != "unk":
        if val["mother"] in referents_linked:
            ref_data["mother"] = referents_linked[val["mother"]]
        else:
            out = generate_referents(val["mother"], referents_dict, referents_linked)
            ref_data["mother"] = out[val["mother"]]

    # Add the father
    if val["father"] != "unk":
        if val["father"] in referents_linked:
            ref_data["father"] = referents_linked[val["father"]]
        else:
            out = {**generate_referents(val["father"], referents_dict, referents_linked), **out}
            ref_data["father"] = out[val["father"]]

    # Add the referent
    out[target] = Referent(target, ref_data)
    return out
    


referents_data = pd.read_csv("family/referents.csv")
records = referents_data.to_dict("records")
priors_data = {record["name"]: record for record in pd.read_csv("family/data/priors.csv").to_dict("records")}
referents_dict = {record["name"]: record for record in records}

referents_linked = {}
for key in referents_dict.keys():
    referents_linked = {**referents_linked, **generate_referents(key, referents_dict, referents_linked)}

origin = referents_linked.pop("origin")

priors = []

for key in referents_linked.keys():
    priors.append(priors_data[key]["prior"]/1467.8)

universe = Universe(tuple(referents_linked.values()), tuple(priors))
