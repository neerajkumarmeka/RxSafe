import sqlite3
from itertools import combinations
from pathlib import Path


# Path to the RxSafe SQLite database
DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "project.db"
)


def get_connection():
    """Create and return a connection to the RxSafe database."""
    return sqlite3.connect(DATABASE_PATH)


def normalize_drug_name(drug_name):
    """Normalize a drug name for consistent searching."""
    return drug_name.strip().lower()


def get_drug(drug_name):
    """Return a drug from the database if it exists."""
    normalized_name = normalize_drug_name(drug_name)

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT drug_id, drug_name
            FROM drugs
            WHERE LOWER(drug_name) = ?
            """,
            (normalized_name,),
        )

        return cursor.fetchone()


def get_all_drugs():
    """Return all drugs in the database alphabetically."""

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT drug_name
            FROM drugs
            ORDER BY drug_name
            """
        )

        return [row[0] for row in cursor.fetchall()]


def check_interaction(drug_a, drug_b):
    """
    Check whether two drugs have a documented interaction.

    Returns a dictionary containing the drugs and severity when an
    interaction exists. Otherwise returns None.
    """

    drug_a = normalize_drug_name(drug_a)
    drug_b = normalize_drug_name(drug_b)

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                d1.drug_name,
                d2.drug_name,
                s.severity_name
            FROM interactions AS i
            JOIN drugs AS d1
                ON i.drug1_id = d1.drug_id
            JOIN drugs AS d2
                ON i.drug2_id = d2.drug_id
            JOIN severity_levels AS s
                ON i.severity_id = s.severity_id
            WHERE
                (
                    LOWER(d1.drug_name) = ?
                    AND LOWER(d2.drug_name) = ?
                )
                OR
                (
                    LOWER(d1.drug_name) = ?
                    AND LOWER(d2.drug_name) = ?
                )
            LIMIT 1
            """,
            (drug_a, drug_b, drug_b, drug_a),
        )

        result = cursor.fetchone()

    if result is None:
        return None

    return {
        "drug_1": result[0],
        "drug_2": result[1],
        "severity": result[2],
    }


def check_multiple_drugs(drugs):
    """
    Check every unique pair in a medication list.

    Returns a list containing documented interactions.
    """

    normalized_drugs = []

    for drug in drugs:
        normalized = normalize_drug_name(drug)

        if normalized and normalized not in normalized_drugs:
            normalized_drugs.append(normalized)

    interactions = []

    for drug_a, drug_b in combinations(normalized_drugs, 2):
        result = check_interaction(drug_a, drug_b)

        if result:
            interactions.append(result)

    return interactions