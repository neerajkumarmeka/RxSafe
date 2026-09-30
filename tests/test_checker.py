from core.checker import (
    normalize_drug_name,
    get_drug,
    check_interaction,
    check_multiple_drugs,
)


def test_normalize_drug_name():
    assert normalize_drug_name("  Abacavir  ") == "abacavir"
    assert normalize_drug_name("ORLISTAT") == "orlistat"


def test_get_existing_drug():
    result = get_drug("Abacavir")

    assert result is not None
    assert result[1] == "Abacavir"


def test_get_drug_case_insensitive():
    result = get_drug("  ABACAVIR  ")

    assert result is not None
    assert result[1] == "Abacavir"


def test_existing_interaction():
    result = check_interaction("Abacavir", "Orlistat")

    assert result is not None
    assert result["severity"] == "Moderate"


def test_interaction_order_independent():
    first = check_interaction("Abacavir", "Orlistat")
    second = check_interaction("Orlistat", "Abacavir")

    assert first == second


def test_interaction_normalizes_input():
    result = check_interaction("   ABACAVIR ", " orlistat   ")

    assert result is not None
    assert result["severity"] == "Moderate"


def test_unknown_interaction():
    result = check_interaction(
        "DefinitelyNotARealDrug",
        "AnotherFakeDrug"
    )

    assert result is None


def test_multiple_drugs():
    results = check_multiple_drugs([
        "Abacavir",
        "Orlistat",
        "Naltrexone",
    ])

    assert isinstance(results, list)
    assert len(results) >= 1