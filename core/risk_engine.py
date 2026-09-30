from collections import Counter

from core.checker import check_multiple_drugs


SEVERITY_WEIGHTS = {
    "Minor": 1,
    "Moderate": 2,
    "Major": 3,
    "Contraindicated": 4,
}

SEVERITY_ORDER = {
    "Minor": 1,
    "Moderate": 2,
    "Major": 3,
    "Contraindicated": 4,
}


def calculate_risk_index(interactions):
    """
    Calculate the RxSafe Risk Index.

    This is a project-specific metric based on documented interaction
    severity and is not a clinically validated risk score.
    """
    return sum(
        SEVERITY_WEIGHTS.get(interaction["severity"], 0)
        for interaction in interactions
    )


def get_highest_severity(interactions):
    """Return the highest severity found among documented interactions."""
    if not interactions:
        return None

    return max(
        (interaction["severity"] for interaction in interactions),
        key=lambda severity: SEVERITY_ORDER.get(severity, 0),
    )


def count_severities(interactions):
    """Count interactions within each severity category."""
    counts = Counter(
        interaction["severity"]
        for interaction in interactions
    )

    return {
        severity: counts.get(severity, 0)
        for severity in SEVERITY_ORDER
    }


def analyze_regimen(drugs):
    """
    Analyze a medication regimen for documented drug-drug interactions.
    """
    cleaned_drugs = []

    for drug in drugs:
        cleaned = drug.strip()

        if cleaned and cleaned.lower() not in [
            existing.lower() for existing in cleaned_drugs
        ]:
            cleaned_drugs.append(cleaned)

    interactions = check_multiple_drugs(cleaned_drugs)

    medication_count = len(cleaned_drugs)
    possible_pairs = (
        medication_count * (medication_count - 1) // 2
    )

    return {
        "medications": cleaned_drugs,
        "medication_count": medication_count,
        "possible_pairs": possible_pairs,
        "interaction_count": len(interactions),
        "severity_counts": count_severities(interactions),
        "highest_severity": get_highest_severity(interactions),
        "risk_index": calculate_risk_index(interactions),
        "interactions": interactions,
    }