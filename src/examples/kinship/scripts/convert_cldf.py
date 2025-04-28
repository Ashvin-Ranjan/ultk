import pandas as pd
from ..meaning import total_names


if __name__ == "__main__":
    # Convert to a DataFrame
    df = pd.DataFrame(columns=["language", "expression"] + total_names)
    lang_data = pd.read_csv("kinship/data/raw_forms.csv", dtype=str, na_filter=False)

    expressions = {}

    for _, row in lang_data.iterrows():
        expression_id = row["Language_ID"] + ":" + row["Form"]
        if row["Parameter_ID"] in total_names:
            if expression_id in expressions:
                expressions[expression_id]["referents"].add(row["Parameter_ID"])
            else:
                expressions[expression_id] = {
                    "lang": row["Language_ID"],
                    "referents": { row["Parameter_ID"] }
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
