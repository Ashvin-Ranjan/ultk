"""Module containing individuals and relations of the kinship domain.

Rather than encoding all the features recursively into Referents, we'll just take advantage of the fact that grammars can be loaded from arbitrary python modules, and reference the data structures here, and keep Referents minimally to contain names.

"""

from typing import Callable

##############################################################################
# Structure class
##############################################################################


class Structure:
    """A general structure for representing a domain and interpretation."""

    def __init__(self, domain: set[str], interpretation: dict[str, Callable]):
        """
        Initialize the structure.

        Args:
            domain (set): The set of Referents.
            interpretation (dict): A mapping of terms to their interpretations.
        """
        self.domain = domain
        self.interpretation = interpretation

    def evaluate(self, term, *args):
        """Evaluate a term on the given arguments."""
        return self.interpretation[term](*args)


##############################################################################
# Define the features of the semantic domain
##############################################################################
domain = {
    "eB",
    "eZ",
    "yB",
    "yZ",
    "F",
    "FF",
    "FM",
    "FeB",
    "FeZ",
    "FyB",
    "FyZ",
    "M",
    "MF",
    "MM",
    "MeB",
    "MeZ",
    "MyB",
    "MyZ",
    "S",
    "D",
    "SS",
    "SD",
    "DD",
    "DS",
    "eBD",
    "eZD",
    "yBD",
    "yZD",
    "eBS",
    "eZS",
    "yBS",
    "yZS",
    "Ego",
}

# Update auxiliary data structures
# Update auxiliary data structures
sex_data = {
    name: (
        name[-1] in ["B", "S", "F"]
        or name == "Ego"
    )
    for name in domain
}


# Age hierarchy: lists of individuals younger or older than each other
age_hierarchy = {
    # Ego's siblings
    "eB": ["Ego", "yB", "yZ"],
    "eZ": ["Ego", "yB", "yZ"],
    "Ego": ["yB", "yZ"],
    "yB": [],
    "yZ": [],
    # Parents' siblings
    "F": ["FyB", "FyZ"],
    "M": ["MyB", "MyZ"],
    "FeB": [
        "F",
        "FyB",
        "FyZ",
    ],
    "FeZ": [
        "F",
        "FyB",
        "FyZ",
    ],
    "FyB": [],
    "FyZ": [],
    "MeB": [
        "M",
        "MyB",
        "MyZ",
    ],
    "MeZ": [
        "M",
        "MyB",
        "MyZ",
    ],
    "MyB": [],
    "MyZ": [],
}

parent_child_data = {
    "FF": [
        "F",
        "FeB",
        "FyB",
        "FeZ",
        "FyZ",
    ],
    "FM": [
        "F",
        "FeB",
        "FyB",
        "FeZ",
        "FyZ",
    ],
    "MF": [
        "M",
        "MeB",
        "MyB",
        "MeZ",
        "MyZ",
    ],
    "MM": [
        "M",
        "MeB",
        "MyB",
        "MeZ",
        "MyZ",
    ],
    "F": [
        "Ego",
        "eB",
        "eZ",
        "yB",
        "yZ",
    ],
    "M": [
        "Ego",
        "eB",
        "eZ",
        "yB",
        "yZ",
    ],
    "Ego": ["S", "D"],
    "S": ["SS", "SD"],
    "D": ["DD", "DS"],
    "SS": [],
    "SD": [],
    "DS": [],
    "DD": [],
    # Parent-child relationships for nieces/nephews
    "eB": ["eBS", "eBD"],
    "eZ": ["eZS", "eZD"],
    "yB": [
        "yBS",
        "yBD",
    ],
    "yZ": [
        "yZS",
        "yZD",
    ],
}


# Interpretation
# just in case lambdas cause issues
def is_male(r: str) -> bool:
    return sex_data[r]


def is_parent(p, c) -> bool:
    return c in parent_child_data.get(p, [])


def is_older(r1, r2) -> bool:
    return r2 in age_hierarchy.get(r1, [])


interpretation = {
    "is_male": is_male,
    "is_parent": is_parent,
    "is_older": is_older,
}
interpretation.update(
    {
        individual: lambda x, individual=individual: individual == x
        for individual in domain
    }
)


##############################################################################
# Testing
##############################################################################
# TODO: use an actual testing framework
def test_structure(kinship_structure, domain, parent_child_data, sex_data):
    """
    Comprehensive test suite to verify the correctness of the kinship structure.

    Args:
        kinship_structure (Structure): The kinship structure.
        domain (dict): Dictionary of Referents in the domain.
        parent_child_data (dict): The parent-child relationship data.
        sex_data (dict): The gender data.
    """

    # print("=== Testing `is_male` Predicate ===")
    for referent in domain:
        expected = sex_data[referent]
        actual = kinship_structure.evaluate("is_male", referent)
        assert (
            actual == expected
        ), f"Failed `is_male` for {referent}: expected {expected}, got {actual}"
        # print(f"PASS: {referent} -> is_male = {actual}")

    # print("\n=== Testing `parent_of` Predicate ===")
    for parent in domain:
        for child in domain:
            expected = child in parent_child_data.get(parent, [])
            actual = kinship_structure.evaluate("is_parent", parent, child)
            assert (
                actual == expected
            ), f"Failed `is_parent` for {parent}, {child.name}: expected {expected}, got {actual}"
            # print(f"PASS: {parent} -> parent_of({child}) = {actual}")

    # print("\n=== Testing `is_older` Predicate ===")
    for r1 in domain:
        for r2 in domain:
            expected = r2 in age_hierarchy.get(r1, [])
            actual = kinship_structure.evaluate("is_older", r1, r2)
            assert (
                actual == expected
            ), f"Failed `is_older` for {r1}, {r2}: expected {expected}, got {actual}"
            # print(f"PASS: {r1} -> is_older({r2}) = {actual}")

    print("\nAll tests passed!")


##############################################################################
# Build
##############################################################################

# Create the structure
kinship_structure = Structure(
    domain=domain,
    interpretation=interpretation,
)

if __name__ == "__main__":

    # Run a minimal test 'suite'
    test_structure(kinship_structure, domain, parent_child_data, sex_data)
