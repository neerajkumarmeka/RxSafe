import pandas as pd
import streamlit as st

from core.analytics import (
    get_database_stats,
    get_severity_distribution,
    get_top_interacting_drugs,
)
from core.checker import (
    check_interaction,
    get_all_drugs,
)
from core.risk_engine import analyze_regimen


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="RxSafe | Drug Interaction Intelligence",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATA
# =========================================================

DRUGS = get_all_drugs()
STATS = get_database_stats()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("💊 RxSafe")

    st.caption("Drug Interaction Intelligence Platform")

    st.divider()

    st.subheader("Database")

    st.metric(
        "Medications",
        f"{STATS['total_drugs']:,}",
    )

    st.metric(
        "Interaction Records",
        f"{STATS['total_interactions']:,}",
    )

    st.divider()

    st.subheader("Technology")

    st.write("Python")
    st.write("SQL / SQLite")
    st.write("Streamlit")
    st.write("Pandas")
    st.write("Pytest")

    st.divider()

    st.caption(
        "Portfolio project demonstrating health informatics, "
        "database engineering, Python development, and "
        "interactive data analysis."
    )


# =========================================================
# HERO
# =========================================================

st.title("💊 RxSafe")

st.markdown(
    "### Drug Interaction Intelligence Platform"
)

st.write(
    "Explore documented drug-drug interactions, analyze "
    "multi-medication regimens, and investigate interaction "
    "patterns using an SQL-backed medication database."
)

hero1, hero2, hero3 = st.columns(3)

hero1.metric(
    "Medications",
    f"{STATS['total_drugs']:,}",
)

hero2.metric(
    "Interaction Records",
    f"{STATS['total_interactions']:,}",
)

hero3.metric(
    "Automated Tests",
    "18",
)

st.info(
    "RxSafe is an educational health informatics portfolio project. "
    "It is not a clinically validated decision-support system and "
    "should not be used independently for treatment decisions."
)

st.divider()


# =========================================================
# NAVIGATION
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🔎 Interaction Checker",
        "💊 Regimen Analyzer",
        "📊 Analytics",
        "ℹ️ About",
    ]
)


# =========================================================
# TAB 1 — INTERACTION CHECKER
# =========================================================

with tab1:
    st.header("Drug Interaction Checker")

    st.write(
        "Select two medications from the database to search "
        "for a documented drug-drug interaction."
    )

    st.caption(
        "Medication names are loaded directly from the RxSafe "
        "SQLite database."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        drug_1 = st.selectbox(
            "First medication",
            options=DRUGS,
            index=None,
            placeholder="Search medication...",
        )

    with col2:
        drug_2 = st.selectbox(
            "Second medication",
            options=DRUGS,
            index=None,
            placeholder="Search medication...",
        )

    check_button = st.button(
        "Check Interaction",
        type="primary",
        width="stretch",
    )

    if check_button:
        if not drug_1 or not drug_2:
            st.error(
                "Select two medications before checking "
                "for an interaction."
            )

        elif drug_1 == drug_2:
            st.error(
                "Select two different medications."
            )

        else:
            with st.spinner(
                "Searching interaction database..."
            ):
                result = check_interaction(
                    drug_1,
                    drug_2,
                )

            st.divider()
            st.subheader("Result")

            if result:
                severity = result["severity"]

                result_col1, result_col2 = st.columns(2)

                result_col1.metric(
                    "Drug Pair",
                    f"{result['drug_1']} + {result['drug_2']}",
                )

                result_col2.metric(
                    "Severity",
                    severity,
                )

                if severity == "Contraindicated":
                    st.error(
                        "Contraindicated interaction documented "
                        "in the current dataset."
                    )

                elif severity == "Major":
                    st.error(
                        "Major interaction documented in the "
                        "current dataset."
                    )

                elif severity == "Moderate":
                    st.warning(
                        "Moderate interaction documented in the "
                        "current dataset."
                    )

                elif severity == "Minor":
                    st.info(
                        "Minor interaction documented in the "
                        "current dataset."
                    )

            else:
                st.success(
                    "No documented interaction was found for "
                    "this drug pair in the current database."
                )

                st.caption(
                    "A missing interaction record does not establish "
                    "that the combination is clinically safe."
                )


# =========================================================
# TAB 2 — REGIMEN ANALYZER
# =========================================================

with tab2:
    st.header("Medication Regimen Analyzer")

    st.write(
        "Select multiple medications to automatically evaluate "
        "every unique drug pair in the regimen."
    )

    st.caption(
        "For n medications, RxSafe evaluates n(n−1)/2 "
        "unique medication pairs."
    )

    st.divider()

    selected_drugs = st.multiselect(
        "Medication regimen",
        options=DRUGS,
        placeholder="Search and add medications...",
    )

    if selected_drugs:
        st.caption(
            f"{len(selected_drugs)} medication(s) selected."
        )

    analyze_button = st.button(
        "Analyze Regimen",
        type="primary",
        width="stretch",
    )

    if analyze_button:
        if len(selected_drugs) < 2:
            st.error(
                "Select at least two medications to analyze "
                "a regimen."
            )

        else:
            with st.spinner(
                "Analyzing medication regimen..."
            ):
                analysis = analyze_regimen(
                    selected_drugs
                )

            st.divider()

            st.subheader("Regimen Overview")

            metric1, metric2, metric3, metric4 = st.columns(4)

            metric1.metric(
                "Medications",
                analysis["medication_count"],
            )

            metric2.metric(
                "Pairs Evaluated",
                analysis["possible_pairs"],
            )

            metric3.metric(
                "Interactions",
                analysis["interaction_count"],
            )

            metric4.metric(
                "RxSafe Risk Index",
                analysis["risk_index"],
            )

            st.caption(
                "The RxSafe Risk Index is a project-specific "
                "educational metric based on interaction severity. "
                "It is not a validated clinical risk score."
            )

            st.divider()

            # ---------------------------------------------
            # Highest severity
            # ---------------------------------------------

            st.subheader("Highest Documented Severity")

            highest_severity = analysis[
                "highest_severity"
            ]

            if highest_severity == "Contraindicated":
                st.error("Contraindicated")

            elif highest_severity == "Major":
                st.error("Major")

            elif highest_severity == "Moderate":
                st.warning("Moderate")

            elif highest_severity == "Minor":
                st.info("Minor")

            else:
                st.success(
                    "No documented interactions identified."
                )

            # ---------------------------------------------
            # Severity distribution
            # ---------------------------------------------

            st.subheader("Regimen Severity Summary")

            severity_df = pd.DataFrame(
                {
                    "Severity": list(
                        analysis[
                            "severity_counts"
                        ].keys()
                    ),
                    "Interactions": list(
                        analysis[
                            "severity_counts"
                        ].values()
                    ),
                }
            )

            severity_col1, severity_col2 = st.columns(
                [1, 1]
            )

            with severity_col1:
                st.dataframe(
                    severity_df,
                    width="stretch",
                    hide_index=True,
                )

            with severity_col2:
                st.bar_chart(
                    severity_df,
                    x="Severity",
                    y="Interactions",
                )

            # ---------------------------------------------
            # Interaction table
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

                severity_rank = {
                    "Contraindicated": 4,
                    "Major": 3,
                    "Moderate": 2,
                    "Minor": 1,
                }

                interaction_df["Severity Rank"] = (
                    interaction_df["Severity"]
                    .map(severity_rank)
                )

                interaction_df = (
                    interaction_df
                    .sort_values(
                        "Severity Rank",
                        ascending=False,
                    )
                    .drop(
                        columns=["Severity Rank"]
                    )
                )

                st.dataframe(
                    interaction_df,
                    width="stretch",
                    hide_index=True,
                )

            else:
                st.success(
                    "No documented interactions were found "
                    "among the selected medications."
                )

                st.caption(
                    "This result does not establish that the "
                    "regimen is clinically safe."
                )


# =========================================================
# TAB 3 — ANALYTICS
# =========================================================

with tab3:
    st.header("Interaction Analytics")

    st.write(
        "Explore aggregate patterns within the RxSafe "
        "drug interaction database."
    )

    st.divider()

    analytics1, analytics2 = st.columns(2)

    analytics1.metric(
        "Medications",
        f"{STATS['total_drugs']:,}",
    )

    analytics2.metric(
        "Unique Interaction Records",
        f"{STATS['total_interactions']:,}",
    )

    st.divider()

    # ---------------------------------------------
    # Severity distribution
    # ---------------------------------------------

    st.subheader("Interaction Severity Distribution")

    severity_data = get_severity_distribution()

    severity_chart_df = pd.DataFrame(
        severity_data
    )

    severity_chart_df.columns = [
        "Severity",
        "Interactions",
    ]

    severity_chart, severity_table = st.columns(
        [2, 1]
    )

    with severity_chart:
        st.bar_chart(
            severity_chart_df,
            x="Severity",
            y="Interactions",
        )

    with severity_table:
        st.dataframe(
            severity_chart_df,
            width="stretch",
            hide_index=True,
        )

    st.divider()

    # ---------------------------------------------
    # Top interacting medications
    # ---------------------------------------------

    st.subheader(
        "Medications with the Most Documented Interactions"
    )

    st.caption(
        "This ranking reflects how frequently a medication "
        "appears in interaction records in this dataset. "
        "It does not represent clinical danger or prescribing risk."
    )

    top_drugs = get_top_interacting_drugs(10)

    top_drugs_df = pd.DataFrame(
        top_drugs
    )

    top_drugs_df.columns = [
        "Medication",
        "Documented Interactions",
    ]

    top_chart, top_table = st.columns(
        [2, 1]
    )

    with top_chart:
        st.bar_chart(
            top_drugs_df,
            x="Medication",
            y="Documented Interactions",
        )

    with top_table:
        st.dataframe(
            top_drugs_df,
            width="stretch",
            hide_index=True,
        )


# =========================================================
# TAB 4 — ABOUT
# =========================================================

with tab4:
    st.header("About RxSafe")

    st.write(
        "RxSafe is a health informatics and software engineering "
        "portfolio project focused on drug interaction data."
    )

    st.divider()

    st.subheader("Project Evolution")

    st.markdown(
        """
        **Drug Interaction Checker v1 — Python**

        The original project implemented drug-pair normalization,
        JSON-based interaction lookup, and multi-medication
        combination checking.

        **Drug Interaction Checker v2 — SQL**

        The database layer introduced a normalized relational
        structure for medications, interaction records, severity
        levels, search logs, indexes, views, and data-import logic.

        **RxSafe — Integrated Platform**

        RxSafe combines the Python application logic with the
        relational database and adds regimen analysis, analytics,
        automated testing, and an interactive Streamlit interface.
        """
    )

    st.divider()

    st.subheader("Architecture")

    st.code(
        """
Streamlit User Interface
          │
          ▼
     Python Core
    /     |      \\
Checker  Risk   Analytics
    \\     |      /
          ▼
      SQLite Database
          │
          ▼
  Drugs + Interactions
        """,
        language=None,
    )

    st.divider()

    st.subheader("Technology Stack")

    tech1, tech2, tech3 = st.columns(3)

    with tech1:
        st.markdown(
            """
            **Application**
            - Python
            - Streamlit
            """
        )

    with tech2:
        st.markdown(
            """
            **Data**
            - SQL
            - SQLite
            - Pandas
            """
        )

    with tech3:
        st.markdown(
            """
            **Quality**
            - Pytest
            - Git
            - GitHub
            """
        )

    st.divider()

    st.subheader("Current Dataset")

    st.write(
        f"RxSafe currently contains "
        f"**{STATS['total_drugs']:,} medications** and "
        f"**{STATS['total_interactions']:,} unique interaction "
        f"records** in its SQLite database."
    )

    st.divider()

    st.subheader("Limitations")

    st.markdown(
        """
        - RxSafe only reports interactions represented in its
          current dataset.
        - Absence of a record does not establish medication safety.
        - Interaction severity alone does not capture all
          patient-specific clinical factors.
        - The RxSafe Risk Index is a project-specific educational
          metric and has not been clinically validated.
        - The platform is not intended to replace professional
          drug-information resources or clinical judgment.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "RxSafe | Drug Interaction Intelligence Platform • "
    "Python • SQL • SQLite • Streamlit • Pandas • Pytest"
)