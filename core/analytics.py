import sqlite3

from core.checker import DATABASE_PATH


def get_database_stats():
    """Return high-level statistics about the RxSafe database."""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM drugs")
        total_drugs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM interactions")
        total_interactions = cursor.fetchone()[0]

    return {
        "total_drugs": total_drugs,
        "total_interactions": total_interactions,
    }


def get_severity_distribution():
    """Return the number of interactions in each severity category."""

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                s.severity_name,
                COUNT(*) AS interaction_count
            FROM interactions AS i
            JOIN severity_levels AS s
                ON i.severity_id = s.severity_id
            GROUP BY s.severity_id, s.severity_name
            ORDER BY s.severity_id
            """
        )

        rows = cursor.fetchall()

    return [
        {
            "severity": row[0],
            "count": row[1],
        }
        for row in rows
    ]


def get_top_interacting_drugs(limit=10):
    """
    Return drugs appearing most frequently in documented interactions.
    """

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                drug_name,
                COUNT(*) AS interaction_count
            FROM (
                SELECT d1.drug_name AS drug_name
                FROM interactions AS i
                JOIN drugs AS d1
                    ON i.drug1_id = d1.drug_id

                UNION ALL

                SELECT d2.drug_name AS drug_name
                FROM interactions AS i
                JOIN drugs AS d2
                    ON i.drug2_id = d2.drug_id
            )
            GROUP BY drug_name
            ORDER BY interaction_count DESC, drug_name ASC
            LIMIT ?
            """,
            (limit,),
        )

        rows = cursor.fetchall()

    return [
        {
            "drug": row[0],
            "interaction_count": row[1],
        }
        for row in rows
    ]