import pandas as pd
from ..meaning import total_names

from itertools import product

def find_alternates(s):
    replacements = [] 
    indicies = []
    for i, c in enumerate(s):
        if c in {"B", "Z"} and (i == 0 or s[i - 1] not in {"e", "y"}):
            replacements.append(("e" + c, "y" + c))
            indicies.append(i)
        elif c == "P":
            replacements.append(("M", "F"))
            indicies.append(i)
        elif c == "C":
            replacements.append(("D", "S"))
            indicies.append(i)


    combinations = [list(p) for p in product(*replacements)]
    
    output = ["" for _ in combinations]
    for i in range(len(s)):
        if len(indicies) > 0 and i == indicies[0]:
            output = [k + combinations[j][0] for j, k in enumerate(output)]
            indicies = indicies[1:]
            combinations = [j[1:] for j in combinations]
        else:
             output = [k + s[i] for k in output]

    
    return output


if __name__ == "__main__":
    # Convert to a DataFrame
    df = pd.DataFrame(columns=["language", "expression"] + total_names)
    lang_data = pd.read_csv("kinship/data/raw_forms.csv", dtype=str, na_filter=False)

    expressions = {}

    for _, row in lang_data.iterrows():
        expression_id = row["Language_ID"] + ":" + row["Form"]
        for alternate in find_alternates(row["Parameter_ID"]):
            if alternate in total_names:
                if expression_id in expressions:
                    expressions[expression_id]["referents"].add(alternate)
                else:
                    expressions[expression_id] = {
                        "lang": row["Language_ID"],
                        "referents": { alternate }
                    }

    expression_meanings = {}

    for term, data in expressions.items():
        if data["lang"] in expression_meanings and data["referents"] in expression_meanings[data["lang"]]:
            continue
        elif data["lang"] in expression_meanings:
            expression_meanings[data["lang"]].append(data["referents"])
        else:
            expression_meanings[data["lang"]] = [ data["referents"] ]
        row = {referent: (referent in data["referents"]) for referent in total_names}
        row["language"] = data["lang"]
        row["expression"] = term
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    fn = "kinship/data/natural_languages.csv"
    df.to_csv(fn, index=False)
    print(f"Wrote to {fn}.")
