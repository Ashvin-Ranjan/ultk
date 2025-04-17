import pandas as pd

from yaml import load, Loader

from ultk.util.io import read_grammatical_expressions, write_languages
from ultk.language.language import Language, FrozenDict, Meaning, Expression

from ..grammar import kinship_grammar
from ..meaning import universe as kinship_universe
from ..measures import comm_cost, complexity


def read_natural_languages(filename: str) -> set[Language]:
    """Read the natural languages from a CSV file.
    Assumes that each row is one expression, with unique strings in "language" column identifying
    which expressions belong to which languages.
    Assumes that there is a boolean-valued column for each Referent in the kinship_universe,
    identified by its name.

    Args:
        filename: the file to read

    Returns:
        a list of Languages
    """
    lang_data = pd.read_csv(filename)
    lang_data["relatives"] = lang_data.apply(
        lambda row: row[row == True].index.tolist(), axis=1
    )
    # group data frame by language
    language_frame = lang_data.groupby("language")
    languages = set()
    # iterate through each language
    for lang, items in language_frame:
        cur_expressions = []
        for item in items.itertuples():
            # generate Meaning from list of relatives
            cur_meaning = Meaning(
                FrozenDict(
                    {
                        referent: referent.name in item.relatives
                        for referent in kinship_universe
                    }
                ),
                kinship_universe,
            )
            # add Expression with form and Meaning
            cur_expressions.append(Expression(item.expression, cur_meaning))
        # add Language with its Expressions
        languages.add(Language(tuple(cur_expressions), name=lang, natural=True))
    return languages

def expression_to_ref_list(expression: Expression):
    out = [] 
    for k, v in expression.meaning.mapping.items():
        if v:
            out.append(k.name)
    return out

if __name__ == "__main__":
    natural_languages = read_natural_languages("kinship/data/natural_languages.csv")
    _, expressions_by_meaning = read_grammatical_expressions(
        "kinship/outputs/generated_expressions.yaml",
        kinship_grammar,
        universe=kinship_universe,
        return_by_meaning=True,
    )
    
    # TODO: Figure out how to deal with languages which are not represented
    representable_languages = set()
    with open("kinship/data/langs_slavic.txt", 'r') as f:
        language_names = f.read().split('\n')

    for language in natural_languages:
        valid = True
        for expression in language.expressions:
            if expression.meaning not in expressions_by_meaning:
                if language.name in language_names:
                    print("Invalid expression:", expression.form, expression_to_ref_list(expression))
                valid = False
        if valid:
            representable_languages.add(language)

    print(f"{len(representable_languages)}/{len(natural_languages)} represented")

    write_languages(
        representable_languages,
        "kinship/outputs/natural_languages.yml",
        {
            "name": lambda _, lang: lang.name,
            "type": lambda _, lang: "natural_check" if lang.name in language_names else "natural",
            "lot_expressions": lambda _, lang: [
                str(expressions_by_meaning[expr.meaning]) for expr in lang.expressions
            ],
            "complexity": lambda _, lang: complexity(lang, expressions_by_meaning),
            "comm_cost": lambda _, lang: comm_cost(lang),
        },
    )
