import pandas as pd
from ..meaning import sorted_names


if __name__ == "__main__":
    # Convert to a DataFrame
    df = pd.DataFrame(columns=["language", "expression"] + sorted_names)
    lang_data = pd.read_csv("kinship/data/raw_forms.csv", dtype=str, na_filter=False)

    expressions = {}

    for _, row in lang_data.iterrows():
        expression_id = row["Language_ID"] + ":" + row["Parameter_ID"][0] + ":" + row["Form"]
        if row["Parameter_ID"][1:] in sorted_names:
            if expression_id in expressions:
                expressions[expression_id]["referents"].add(row["Parameter_ID"][1:])
            else:
                expressions[expression_id] = {
                    "lang": row["Language_ID"] + ":" + row["Parameter_ID"][0],
                    "referents": { row["Parameter_ID"][1:] }
                }


    for term, data in expressions.items():
        row = {referent: (referent in data["referents"]) for referent in sorted_names}
        row["language"] = data["lang"]
        row["expression"] = term
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    fn = "kinship/data/natural_languages.csv"
    df.to_csv(fn, index=False)
    print(f"Wrote to {fn}.")
