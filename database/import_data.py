import sqlite3
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

# Directory containing this script
BASE_DIR = Path(__file__).resolve().parent

# SQLite database stored in the same directory
DATABASE_PATH = BASE_DIR / "project.db"

# DDInter source files used by the current RxSafe dataset
DATA_FILES = [
    BASE_DIR / "ddinter_downloads_code_A.csv",
    BASE_DIR / "ddinter_downloads_code_V.csv",
]


# ---------------------------------------------------------
# Severity mapping
# ---------------------------------------------------------

def severity_to_id(level):
    """Convert DDInter severity labels to RxSafe severity IDs."""

    if pd.isna(level):
        return None

    level = str(level).strip().title()

    mapping = {
        "Minor": 1,
        "Moderate": 2,
        "Major": 3,
        "Contraindicated": 4,
    }

    return mapping.get(level)


# ---------------------------------------------------------
# CSV importer
# ---------------------------------------------------------

def import_csv(filename, conn):
    """Import one DDInter CSV file into the RxSafe database."""

    df = pd.read_csv(filename)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        drug1_id = row["DDInterID_A"]
        drug1_name = row["Drug_A"]

        drug2_id = row["DDInterID_B"]
        drug2_name = row["Drug_B"]

        level = row["Level"]
        severity_id = severity_to_id(level)

        if severity_id is None:
            print(f"Skipping unknown severity: {level}")
            continue

        # Insert first drug if it does not already exist
        cursor.execute(
            """
            INSERT OR IGNORE INTO drugs (
                drug_id,
                drug_name
            )
            VALUES (?, ?)
            """,
            (drug1_id, drug1_name),
        )

        # Insert second drug if it does not already exist
        cursor.execute(
            """
            INSERT OR IGNORE INTO drugs (
                drug_id,
                drug_name
            )
            VALUES (?, ?)
            """,
            (drug2_id, drug2_name),
        )

        # Insert interaction while preventing duplicates
        cursor.execute(
            """
            INSERT OR IGNORE INTO interactions (
                drug1_id,
                drug2_id,
                severity_id,
                interaction_description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                drug1_id,
                drug2_id,
                severity_id,
                None,
            ),
        )

    conn.commit()

    print(f"Imported: {filename.name}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    """Import the selected DDInter datasets into RxSafe."""

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"RxSafe database not found: {DATABASE_PATH}"
        )

    missing_files = [
        file_path
        for file_path in DATA_FILES
        if not file_path.exists()
    ]

    if missing_files:
        missing_names = ", ".join(
            file_path.name
            for file_path in missing_files
        )

        raise FileNotFoundError(
            f"Missing DDInter source file(s): {missing_names}"
        )

    with sqlite3.connect(DATABASE_PATH) as conn:
        for file_path in DATA_FILES:
            import_csv(file_path, conn)

    print("Data imported successfully!")


if __name__ == "__main__":
    main()