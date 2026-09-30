import pandas as pd
import sqlite3


def severity_to_id(level):
    if pd.isna(level):
        return None

    level = str(level).strip().title()

    mapping = {
        "Minor": 1,
        "Moderate": 2,
        "Major": 3,
        "Contraindicated": 4
    }

    return mapping.get(level)


def import_csv(filename, conn):
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

        cursor.execute("""
            INSERT OR IGNORE INTO drugs (drug_id, drug_name)
            VALUES (?, ?)
        """, (drug1_id, drug1_name))

        cursor.execute("""
            INSERT OR IGNORE INTO drugs (drug_id, drug_name)
            VALUES (?, ?)
        """, (drug2_id, drug2_name))

        cursor.execute("""
            INSERT OR IGNORE INTO interactions (
                drug1_id,
                drug2_id,
                severity_id,
                interaction_description
            )
            VALUES (?, ?, ?, ?)
        """, (drug1_id, drug2_id, severity_id, None))

    conn.commit()


def main():
    conn = sqlite3.connect("project.db")

    import_csv("ddinter_downloads_code_A.csv", conn)
    import_csv("ddinter_downloads_code_V.csv", conn)

    conn.close()
    print("Data imported successfully!")


if __name__ == "__main__":
    main()
