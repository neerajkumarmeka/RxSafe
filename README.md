# 💊 RxSafe

### Drug Interaction Intelligence Platform

RxSafe is a health informatics and software engineering portfolio project that combines Python, SQL, SQLite, Streamlit, and data analytics to explore documented drug-drug interactions.

The platform allows users to search for interactions between two medications, analyze multi-drug regimens, summarize interaction severity, and explore aggregate patterns within a relational drug interaction database.

> **Disclaimer:** RxSafe is an educational and portfolio project. It is not a clinically validated decision-support system and should not be used independently to make medication or treatment decisions.

---

## Overview

Medication regimens can contain multiple possible drug-drug combinations. As the number of medications increases, manually evaluating every pair becomes increasingly difficult.

For `n` medications, the number of unique pairs is:

```text
n(n - 1) / 2
```

RxSafe automates this process by generating every unique medication pair and querying a relational SQLite database for documented interactions.

The current database contains:

- **1,798 medications**
- **48,930 unique interaction records**
- Four interaction severity categories:
  - Minor
  - Moderate
  - Major
  - Contraindicated

---

## Features

### 🔎 Drug Interaction Checker

Search and select two medications from the database and check whether a documented interaction exists.

The application:

- supports searchable medication selection
- performs case-normalized database lookup
- checks the drug pair in either stored direction
- reports documented interaction severity
- distinguishes missing interaction records from evidence of clinical safety

---

### 💊 Medication Regimen Analyzer

Select multiple medications and automatically evaluate every unique medication pair.

For example, four medications generate six unique pairs:

```text
A ↔ B
A ↔ C
A ↔ D
B ↔ C
B ↔ D
C ↔ D
```

The analyzer reports:

- number of medications
- number of pairs evaluated
- number of documented interactions
- highest documented severity
- severity distribution
- interaction-level results
- RxSafe Risk Index

---

## RxSafe Risk Index

RxSafe includes a project-specific educational metric that summarizes documented interaction severity within a medication regimen.

The current weighting system is:

| Severity | Weight |
|---|---:|
| Minor | 1 |
| Moderate | 2 |
| Major | 3 |
| Contraindicated | 4 |

The index is calculated by summing the weights of documented interactions identified within the selected regimen.

**The RxSafe Risk Index is not a clinically validated risk score.** It is included to demonstrate transparent rule-based aggregation and should not be interpreted as a patient-specific clinical risk assessment.

---

## 📊 Interaction Analytics

The analytics dashboard provides aggregate insights into the interaction database, including:

- total medications
- total unique interaction records
- interaction severity distribution
- medications appearing most frequently in documented interaction records

Frequency in the dataset should not be interpreted as a ranking of medication safety or clinical danger.

---

## Architecture

```text
                   RxSafe
                     │
                     ▼
             Streamlit Interface
                     │
                     ▼
                Python Core
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
       Checker      Risk     Analytics
                    Engine
          │          │          │
          └──────────┼──────────┘
                     │
                     ▼
              SQLite Database
          ┌──────────┼──────────┐
          │          │          │
        Drugs   Interactions  Severity
```

---

## Project Evolution

RxSafe evolved from two earlier projects focused separately on programming logic and relational database design.

### Drug Interaction Checker v1 — Python

The first version was developed as a Python project and introduced:

- drug-pair normalization
- JSON-based interaction lookup
- multi-drug combination generation
- automated Python tests

### Drug Interaction Checker v2 — SQL

The second version moved the interaction data into a relational SQLite architecture and introduced:

- normalized database tables
- primary and foreign keys
- interaction severity relationships
- indexes
- SQL views
- triggers
- Python-based CSV import
- duplicate prevention

### RxSafe

RxSafe integrates and extends these concepts into a single interactive platform:

```text
Python interaction logic
          +
Relational SQL database
          +
Regimen analysis
          +
Data analytics
          +
Streamlit interface
          +
Automated testing
```

---

## Database Design

RxSafe uses SQLite as its relational data layer.

### `drugs`

Stores unique medication identifiers and names.

```text
drug_id
drug_name
```

### `severity_levels`

Stores standardized interaction severity categories.

```text
severity_id
severity_name
```

### `interactions`

Connects medication pairs with documented severity.

```text
interaction_id
drug1_id
drug2_id
severity_id
interaction_description
```

Foreign keys connect interaction records to the medication and severity tables.

A uniqueness constraint helps prevent duplicate drug-pair/severity records.

### `search_logs`

Provides a structure for recording medication searches.

```text
log_id
searched_drugs
search_timestamp
```

---

## Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Database | SQLite |
| Query Language | SQL |
| Web Application | Streamlit |
| Data Processing | Pandas |
| Testing | Pytest |
| Version Control | Git |
| Repository | GitHub |

---

## Project Structure

```text
RxSafe/
│
├── app.py
│
├── core/
│   ├── __init__.py
│   ├── checker.py
│   ├── risk_engine.py
│   └── analytics.py
│
├── database/
│   ├── project.db
│   ├── schema.sql
│   ├── queries.sql
│   └── import_data.py
│
├── tests/
│   ├── __init__.py
│   ├── test_checker.py
│   ├── test_risk_engine.py
│   └── test_analytics.py
│
├── assets/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/neerajkumarmeka/RxSafe.git
```

Enter the project directory:

```bash
cd RxSafe
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Running RxSafe

Start the Streamlit application:

```bash
streamlit run app.py
```

Then open the address provided by Streamlit in your browser.

---

## Automated Testing

RxSafe includes automated tests for:

- medication normalization
- medication lookup
- case-insensitive searching
- two-drug interaction detection
- reversed drug-pair detection
- multi-drug analysis
- duplicate medication handling
- severity aggregation
- RxSafe Risk Index calculation
- database statistics
- analytics queries

Run the complete test suite with:

```bash
python -m pytest -v
```

Current test suite:

```text
18 tests
```

---

## Example Workflow

### Interaction Checker

```text
Abacavir
+
Orlistat
        ↓
RxSafe SQL Interaction Engine
        ↓
Documented Interaction
        ↓
Moderate
```

### Regimen Analyzer

```text
Medication A
Medication B
Medication C
Medication D
        ↓
Generate all unique pairs
        ↓
Query SQLite interaction database
        ↓
Aggregate documented interactions
        ↓
Severity Summary + RxSafe Risk Index
```

---

## Limitations

RxSafe has several important limitations:

- It only identifies interactions represented in the current dataset.
- Absence of an interaction record does not establish medication safety.
- Interaction severity does not incorporate patient-specific factors such as age, renal function, hepatic function, dose, indication, genetics, laboratory results, or comorbidities.
- The RxSafe Risk Index has not been clinically validated.
- Dataset frequency should not be interpreted as medication danger or prescribing risk.
- RxSafe is not intended to replace validated clinical decision-support systems, professional drug-information resources, pharmacists, physicians, or other qualified healthcare professionals.

---

## Future Development

Potential future extensions include:

- interaction descriptions and clinical management information
- medication autocomplete enhancements
- patient-specific clinical variables
- interaction search history
- additional analytics
- external drug terminology/API integration
- containerized deployment
- expanded automated testing
- clinically validated data-source integration

---

## Author

**Neeraj Kumar Meka**

Pharm.D. | M.S. Health Informatics

Interests include clinical informatics, healthcare data analytics, clinical decision support, database systems, and healthcare software development.

---

## License

This project is intended for educational and portfolio use.