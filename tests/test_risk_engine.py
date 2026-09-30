from core.risk_engine import (
    calculate_risk_index,
    get_highest_severity,
    count_severities,
    analyze_regimen,
)


SAMPLE_INTERACTIONS = [
    {
        "drug_1": "Drug A",
        "drug_2": "Drug B",
        "severity": "Minor",
    },
    {
        "drug_1": "Drug A",
        "drug_2": "Drug C",
        "severity": "Major",
    },
    {
        "drug_1": "Drug B",
        "drug_2": "Drug C",
        "severity": "Moderate",
    },
]


def test_calculate_risk_index():
    assert calculate_risk_index(SAMPLE_INTERACTIONS) == 6


def test_highest_severity():
    assert get_highest_severity(SAMPLE_INTERACTIONS) == "Major"


def test_highest_severity_empty():
    assert get_highest_severity([]) is None


def test_count_severities():
    counts = count_severities(SAMPLE_INTERACTIONS)

    assert counts["Minor"] == 1
    assert counts["Moderate"] == 1
    assert counts["Major"] == 1
    assert counts["Contraindicated"] == 0


def test_analyze_regimen():
    result = analyze_regimen([
        "Abacavir",
        "Orlistat",
        "Naltrexone",
    ])

    assert result["medication_count"] == 3
    assert result["possible_pairs"] == 3
    assert isinstance(result["interactions"], list)


def test_duplicate_drugs_removed():
    result = analyze_regimen([
        "Abacavir",
        "abacavir",
        "  ABACAVIR ",
        "Orlistat",
    ])

    assert result["medication_count"] == 2
    assert result["possible_pairs"] == 1