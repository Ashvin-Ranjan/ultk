import pandas as pd

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def yaml_to_dataframe(filename: str, keys: list[str]) -> pd.DataFrame:
    with open(filename, "r") as f:
        language_dicts = load(f, Loader=Loader)
    return pd.DataFrame.from_records(
        [{key: lang_dict[key] for key in keys} for lang_dict in language_dicts]
    )


if __name__ == "__main__":
    keys = ["name", "comm_cost", "complexity", "type"]
    dominating_languages = yaml_to_dataframe(
        "kinship/outputs/dominating_languages.yml", keys
    )
    explored_languages = yaml_to_dataframe(
        "kinship/outputs/explored_languages.yml", keys
    )
    drift_languages = yaml_to_dataframe(
        "kinship/outputs/random_drift.yml", keys
    )
    dominating_languages["level"] = 0
    explored_languages["level"] = 0
    drift_languages["level"] = 0
    natural_languages = yaml_to_dataframe("kinship/outputs/natural_languages.yml", keys + ["level"])
    all_data = pd.concat(
        [explored_languages, dominating_languages, natural_languages, drift_languages],
        ignore_index=True,
    )
    all_data.to_csv("kinship/outputs/combined_data.csv", index=False)
