import pandas as pd
import streamlit as st

from core.checker import (
    check_interaction,
    get_all_drugs,
)
from core.risk_engine import analyze_regimen


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RxSafe",
    page_icon="💊",
    layout="wide",
)


# =========================================================
# LOAD DRUG CATALOG
# =========================================================

DRUGS = get_all_drugs()


# =========================================================
# HEADER
# =========================================================

st.title("💊 RxSafe")
st.subheader("Drug Interaction Intelligence Platform")

st.caption(
    "A health informatics portfolio project for exploring documented "
    "drug-drug interactions and medication regimen risk."
)

st.warning(
    "Educational and informational use only. RxSafe is not a substitute "
    "for professional medical judgment or a validated clinical decision "
    "support system."
)

st.divider()


# =========================================================
# NAVIGATION
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "Interaction Checker",
        "Regimen Analyzer",
        "About RxSafe",
    ]
)


# =========================================================
# TAB 1 — TWO-DRUG INTERACTION CHECKER
# =========================================================

with tab1:
    st.header("Drug Interaction Checker")

    st.write(
        "Search and select two medications to check for a documented "
        "drug-drug interaction."
    )

    col1, col2 = st.columns(2)

    with col1:
        drug_1 = st.selectbox(
            "Drug 1",
            options=DRUGS,
            index=None,
            placeholder="Search for a medication...",
        )

    with col2:
        drug_2 = st.selectbox(
            "Drug 2",
            options=DRUGS,
            index=None,
            placeholder="Search for a medication...",
        )

    if st.button(
        "Check Interaction",
        type="primary",
        width="stretch",
    ):
        if not drug_1 or not drug_2:
            st.error("Please select both medications.")

        elif drug_1 == drug_2:
            st.error("Please select two different medications.")

        else:
            result = check_interaction(drug_1, drug_2)

            if result:
                severity = result["severity"]

                if severity in ("Contraindicated", "Major"):
                    st.error(
                        f"Interaction found — {severity}"
                    )

                elif severity == "Moderate":
                    st.warning(
                        f"Interaction found — {severity}"
                    )

                else:
                    st.info(
                        f"Interaction found — {severity}"
                    )

                st.write(
                    f"**{result['drug_1']} ↔ "
                    f"{result['drug_2']}**"
                )

                st.write(
                    f"Documented severity: **{severity}**"
                )

            else:
                st.success(
                    "No documented interaction was found for this "
                    "drug pair in the current database."
                )

                st.caption(
                    "Absence from this dataset does not establish "
                    "that a drug combination is clinically safe."
                )


# =========================================================
# TAB 2 — MULTI-DRUG REGIMEN ANALYZER
# =========================================================

with tab2:
    st.header("Medication Regimen Analyzer")

    st.write(
        "Select multiple medications and RxSafe will evaluate every "
        "unique drug pair for documented interactions."
    )

    selected_drugs = st.multiselect(
        "Select medications",
        options=DRUGS,
        placeholder="Search and add medications...",
    )

    if st.button(
        "Analyze Regimen",
        type="primary",
        width="stretch",
    ):
        drugs = selected_drugs

        if len(drugs) < 2:
            st.error(
                "Select at least two medications to analyze a regimen."
            )

        else:
            analysis = analyze_regimen(drugs)

            st.subheader("Regimen Overview")

            metric1, metric2, metric3, metric4 = st.columns(4)

            metric1.metric(
                "Medications",
                analysis["medication_count"],
            )

            metric2.metric(
                "Pairs Checked",
                analysis["possible_pairs"],
            )

            metric3.metric(
                "Interactions Found",
                analysis["interaction_count"],
            )

            metric4.metric(
                "RxSafe Risk Index",
                analysis["risk_index"],
            )

            st.caption(
                "The RxSafe Risk Index is a project-specific educational "
                "metric derived from documented interaction severities. "
                "It is not a clinically validated risk score."
            )

            st.divider()

            # ---------------------------------------------
            # Highest severity
            # ---------------------------------------------

            st.subheader("Highest Documented Severity")

            severity = analysis["highest_severity"]

            if severity:
                if severity in ("Contraindicated", "Major"):
                    st.error(severity)

                elif severity == "Moderate":
                    st.warning(severity)

                else:
                    st.info(severity)

            else:
                st.success(
                    "No documented interactions were identified."
                )

            # ---------------------------------------------
            # Severity summary
            # ---------------------------------------------

            st.subheader("Severity Summary")

            severity_df = pd.DataFrame(
                {
                    "Severity": list(
                        analysis["severity_counts"].keys()
                    ),
                    "Interactions": list(
                        analysis["severity_counts"].values()
                    ),
                }
            )

            st.dataframe(
                severity_df,
                width="stretch",
                hide_index=True,
            )

            # ---------------------------------------------
            # Interaction results
            # ---------------------------------------------

            st.subheader("Documented Interactions")

            if analysis["interactions"]:
                interaction_df = pd.DataFrame(
                    analysis["interactions"]
                )

                interaction_df.columns = [
                    "Drug 1",
                    "Drug 2",
                    "Severity",
                ]

                st.dataframe(
                    interaction_df,
                    width="stretch",
                    hide_index=True,
                )

            else:
                st.success(
                    "No documented interactions were found among "
                    "the selected medications."
                )

                st.caption(
                    "This result does not establish that the medication "
                    "regimen is clinically safe."
                )


# =========================================================
# TAB 3 — ABOUT RXSAFE
# =========================================================

with tab3:
    st.header("About RxSafe")

    st.markdown(
        """
        **RxSafe** is a Drug Interaction Intelligence Platform developed
        as a health informatics and software engineering portfolio project.

        ### Project Evolution

        **Drug Interaction Checker v1 — CS50P**

        - Python-based interaction checking
        - Drug-pair normalization
        - Multi-drug combination analysis
        - JSON-based interaction storage

        **Drug Interaction Checker v2 — CS50 SQL**

        - Relational SQLite database
        - Normalized drug and interaction tables
        - SQL joins and views
        - Database indexes
        - Triggers
        - Python-based data import

        **RxSafe**

        - SQL-backed Python interaction engine
        - Searchable medication catalog
        - Two-drug interaction checking
        - Multi-drug regimen analysis
        - Severity summarization
        - RxSafe Risk Index
        - Interactive Streamlit interface
        - Automated testing

        ### Technology Stack

        **Python • SQL • SQLite • Streamlit • Pandas • Pytest**

        ### Safety

        RxSafe is an educational and portfolio project. Interaction
        information should not be used independently to make medication
        or treatment decisions. Clinical decisions should be made using
        appropriate professional resources and qualified healthcare
        professionals.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "RxSafe — Drug Interaction Intelligence Platform | "
    "Built with Python, SQL, SQLite, Streamlit, and Pandas"
)