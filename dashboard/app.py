from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="HR Career Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================
# Works when this file is:
#   i_project/dashboard/app.py
# and also when it is accidentally inside:
#   i_project/dashboard/dashboard/app.py
#
# The candidate-path logic below makes the app more robust.
APP_DIR = Path(__file__).resolve().parent

PROJECT_ROOT_CANDIDATES = [
    APP_DIR.parent,
    APP_DIR.parent.parent,
    Path.cwd(),
]

FINAL_FILENAME = "hr_career_risk_analysis.csv"
FEATURE_FILENAME = "feature_engineered_palo_alto.csv"


def find_data_file(filename: str):
    """Find a project data file without depending on the current terminal directory."""
    checked = []

    for root in PROJECT_ROOT_CANDIDATES:
        candidate = root / "data" / filename
        checked.append(candidate)
        if candidate.exists():
            return candidate

    return None


# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    """
    Prefer the Day 6 final dataset.
    Fall back to Day 4 feature-engineered data only when necessary.
    """
    final_path = find_data_file(FINAL_FILENAME)

    if final_path is not None:
        data = pd.read_csv(final_path)
        return data, final_path, "Day 6 final dataset"

    feature_path = find_data_file(FEATURE_FILENAME)

    if feature_path is not None:
        data = pd.read_csv(feature_path)
        return data, feature_path, "Day 4 fallback dataset"

    checked_paths = "\n".join(
        f"- {root / 'data' / FINAL_FILENAME}"
        for root in PROJECT_ROOT_CANDIDATES
    )

    raise FileNotFoundError(
        "No dashboard dataset was found.\n\n"
        "Expected the Day 6 file:\n"
        f"data/{FINAL_FILENAME}\n\n"
        "Checked:\n"
        f"{checked_paths}"
    )


def safe_rate(numerator, denominator):
    """Return a percentage safely."""
    if denominator == 0:
        return 0.0
    return numerator / denominator * 100


def sorted_unique(series):
    """Return stable string-sorted unique values for Streamlit filters."""
    values = series.dropna().unique().tolist()
    return sorted(values, key=lambda x: str(x).lower())


# ============================================================
# VALIDATION
# ============================================================
def validate_dataset(data):
    """Validate only columns required for dashboard functionality."""
    required_for_core = [
        "Attrition",
        "YearsAtCompany",
    ]

    missing_core = [c for c in required_for_core if c not in data.columns]

    if missing_core:
        raise ValueError(
            "The loaded dataset is missing required columns: "
            + ", ".join(missing_core)
        )


# ============================================================
# FILTERS
# ============================================================
def apply_filters(data):
    """Apply optional sidebar filters without assuming every column exists."""
    st.sidebar.header("🔎 Filters")

    filtered = data.copy()

    if "Department" in filtered.columns:
        options = sorted_unique(filtered["Department"])
        selected = st.sidebar.multiselect(
            "Department",
            options,
            default=options,
        )
        filtered = filtered[filtered["Department"].isin(selected)]

    if "JobRole" in filtered.columns:
        options = sorted_unique(filtered["JobRole"])
        selected = st.sidebar.multiselect(
            "Job Role",
            options,
            default=options,
        )
        filtered = filtered[filtered["JobRole"].isin(selected)]

    if "JobLevel" in filtered.columns:
        options = sorted_unique(filtered["JobLevel"])
        selected = st.sidebar.multiselect(
            "Job Level",
            options,
            default=options,
        )
        filtered = filtered[filtered["JobLevel"].isin(selected)]

    if "CareerStage" in filtered.columns:
        # Convert both options and data to strings so category/object
        # dtypes do not cause filter mismatches.
        stage_values = filtered["CareerStage"].dropna().astype(str)
        options = sorted(stage_values.unique().tolist())
        selected = st.sidebar.multiselect(
            "Career Stage",
            options,
            default=options,
        )
        filtered = filtered[
            filtered["CareerStage"].astype(str).isin(selected)
        ]

    if "CareerCluster" in filtered.columns:
        options = sorted_unique(filtered["CareerCluster"])
        selected = st.sidebar.multiselect(
            "Career Cluster",
            options,
            default=options,
        )
        filtered = filtered[filtered["CareerCluster"].isin(selected)]

    if "PromotionGapRiskLevel" in filtered.columns:
        preferred_order = ["Low", "Medium", "High"]
        present = set(
            filtered["PromotionGapRiskLevel"]
            .dropna()
            .astype(str)
            .tolist()
        )
        options = [x for x in preferred_order if x in present]

        selected = st.sidebar.multiselect(
            "Risk Level",
            options,
            default=options,
        )
        filtered = filtered[
            filtered["PromotionGapRiskLevel"].astype(str).isin(selected)
        ]

    if "RetentionOpportunityLevel" in filtered.columns:
        preferred_order = ["Low", "Medium", "High"]
        present = set(
            filtered["RetentionOpportunityLevel"]
            .dropna()
            .astype(str)
            .tolist()
        )
        options = [x for x in preferred_order if x in present]

        selected = st.sidebar.multiselect(
            "Retention Opportunity",
            options,
            default=options,
        )
        filtered = filtered[
            filtered["RetentionOpportunityLevel"].astype(str).isin(selected)
        ]

    return filtered


# ============================================================
# LOAD DATA
# ============================================================
try:
    df, source_path, source_type = load_data()
    validate_dataset(df)
except Exception as exc:
    st.error("Dashboard data could not be loaded.")
    st.code(str(exc))
    st.info(
        "Run the Day 6 notebook first and make sure the final CSV is inside "
        "the project's data/ folder."
    )
    st.stop()


# ============================================================
# HEADER
# ============================================================
st.title("📊 HR Career Analytics Dashboard")
st.caption(
    "Career progression • promotion gaps • employee clustering • "
    "risk & retention opportunities"
)

st.sidebar.caption(f"Data source: {source_path.name}")
if source_type == "Day 4 fallback dataset":
    st.sidebar.warning(
        "Day 6 final dataset was not found. "
        "Risk/retention and cluster sections may be unavailable."
    )


# ============================================================
# FILTER DATA
# ============================================================
filtered = apply_filters(df)

if filtered.empty:
    st.warning(
        "No employees match the selected filters. "
        "Adjust the filters in the sidebar."
    )
    st.stop()


# ============================================================
# KPI ROW
# ============================================================
total_employees = len(filtered)

attrition_rate = (
    safe_rate(
        (filtered["Attrition"].astype(str).str.strip().eq("Yes")).sum(),
        total_employees,
    )
    if "Attrition" in filtered.columns
    else 0.0
)

avg_tenure = (
    pd.to_numeric(filtered["YearsAtCompany"], errors="coerce").mean()
    if "YearsAtCompany" in filtered.columns
    else 0.0
)

high_risk = (
    filtered["PromotionGapRiskLevel"]
    .astype(str)
    .eq("High")
    .sum()
    if "PromotionGapRiskLevel" in filtered.columns
    else 0
)

high_opportunity = (
    filtered["RetentionOpportunityLevel"]
    .astype(str)
    .eq("High")
    .sum()
    if "RetentionOpportunityLevel" in filtered.columns
    else 0
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Employees", f"{total_employees:,}")
c2.metric("Attrition Rate", f"{attrition_rate:.1f}%")
c3.metric("Avg. Years at Company", f"{avg_tenure:.1f}")
c4.metric("High Promotion Risk", f"{high_risk:,}")
c5.metric("High Retention Opportunity", f"{high_opportunity:,}")


# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏠 Executive Overview",
        "👥 Workforce Analysis",
        "📈 Career Progression",
        "🤖 Career Clusters",
        "🎯 Risk & Retention",
    ]
)


# ============================================================
# TAB 1 — EXECUTIVE OVERVIEW
# ============================================================
with tab1:
    st.subheader("Executive Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Employees by Department")
        if "Department" in filtered.columns:
            dept = (
                filtered["Department"]
                .value_counts()
                .rename("Employees")
            )
            st.bar_chart(dept)

    with col2:
        st.markdown("### Attrition")
        if "Attrition" in filtered.columns:
            attr = (
                filtered["Attrition"]
                .astype(str)
                .str.strip()
                .value_counts()
                .rename("Employees")
            )
            st.bar_chart(attr)

    st.markdown("### Promotion Risk")
    if "PromotionGapRiskLevel" in filtered.columns:
        risk = (
            filtered["PromotionGapRiskLevel"]
            .astype(str)
            .value_counts()
            .reindex(["Low", "Medium", "High"])
            .fillna(0)
            .astype(int)
        )
        st.bar_chart(risk)
    else:
        st.info("Promotion risk fields are not available in this dataset.")


# ============================================================
# TAB 2 — WORKFORCE ANALYSIS
# ============================================================
with tab2:
    st.subheader("Workforce Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Job Role Distribution")
        if "JobRole" in filtered.columns:
            role = (
                filtered["JobRole"]
                .value_counts()
                .sort_values()
            )
            st.bar_chart(role)

    with col2:
        st.markdown("### Job Level Distribution")
        if "JobLevel" in filtered.columns:
            level = (
                filtered["JobLevel"]
                .value_counts()
                .sort_index()
            )
            st.bar_chart(level)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Age Distribution")
        if "Age" in filtered.columns:
            age = pd.to_numeric(filtered["Age"], errors="coerce").dropna()

            if not age.empty:
                age_hist = (
                    pd.cut(age, bins=10, include_lowest=True)
                    .value_counts()
                    .sort_index()
                    .rename("Employees")
                )
                age_hist.index = age_hist.index.astype(str)
                st.bar_chart(age_hist)
            else:
                st.info("No valid Age values available.")

    with col4:
        st.markdown("### Career Stage")
        if "CareerStage" in filtered.columns:
            stage = (
                filtered["CareerStage"]
                .astype(str)
                .value_counts()
            )
            st.bar_chart(stage)


# ============================================================
# TAB 3 — CAREER PROGRESSION
# ============================================================
with tab3:
    st.subheader("Career Progression")

    metric_cols = st.columns(4)

    progression_metrics = [
        ("Avg. Years at Company", "YearsAtCompany"),
        ("Avg. Years in Current Role", "YearsInCurrentRole"),
        ("Avg. Years Since Promotion", "YearsSinceLastPromotion"),
        ("Avg. Years with Current Manager", "YearsWithCurrManager"),
    ]

    for container, (label, column) in zip(
        metric_cols,
        progression_metrics,
    ):
        if column in filtered.columns:
            value = pd.to_numeric(
                filtered[column],
                errors="coerce",
            ).mean()
        else:
            value = 0.0

        container.metric(label, f"{value:.1f}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Average Promotion Gap by Department")
        if {"Department", "YearsSinceLastPromotion"}.issubset(
            filtered.columns
        ):
            promotion = (
                filtered.assign(
                    YearsSinceLastPromotion=pd.to_numeric(
                        filtered["YearsSinceLastPromotion"],
                        errors="coerce",
                    )
                )
                .groupby("Department")["YearsSinceLastPromotion"]
                .mean()
                .sort_values()
            )
            st.bar_chart(promotion)

    with col2:
        st.markdown("### Average Time in Current Role by Department")
        if {"Department", "YearsInCurrentRole"}.issubset(
            filtered.columns
        ):
            role_time = (
                filtered.assign(
                    YearsInCurrentRole=pd.to_numeric(
                        filtered["YearsInCurrentRole"],
                        errors="coerce",
                    )
                )
                .groupby("Department")["YearsInCurrentRole"]
                .mean()
                .sort_values()
            )
            st.bar_chart(role_time)

    st.markdown("### Promotion Gap Groups")
    if "PromotionGapGroup" in filtered.columns:
        gap_group = (
            filtered["PromotionGapGroup"]
            .astype(str)
            .value_counts()
        )
        st.bar_chart(gap_group)

    st.markdown("### Career Progression Data")

    progression_cols = [
        c
        for c in [
            "Department",
            "JobRole",
            "JobLevel",
            "CareerStage",
            "YearsAtCompany",
            "YearsInCurrentRole",
            "YearsSinceLastPromotion",
            "PromotionGapRatio",
            "RoleStagnationRatio",
        ]
        if c in filtered.columns
    ]

    if progression_cols:
        st.dataframe(
            filtered[progression_cols],
            use_container_width=True,
        )


# ============================================================
# TAB 4 — CAREER CLUSTERS
# ============================================================
with tab4:
    st.subheader("Career Clusters")

    if "CareerCluster" not in filtered.columns:
        st.info(
            "CareerCluster is not present. "
            "Run Day 5 clustering and connect its output to Day 6."
        )
    else:
        cluster_summary = (
            filtered.groupby("CareerCluster", observed=True)
            .agg(
                Employees=("CareerCluster", "size"),
                Avg_YearsAtCompany=("YearsAtCompany", "mean"),
                Avg_YearsInCurrentRole=("YearsInCurrentRole", "mean"),
                Avg_YearsSinceLastPromotion=(
                    "YearsSinceLastPromotion",
                    "mean",
                ),
                Avg_JobLevel=("JobLevel", "mean"),
            )
            .round(2)
        )

        st.dataframe(
            cluster_summary,
            use_container_width=True,
        )

        st.markdown("### Employees by Career Cluster")

        cluster_counts = (
            filtered["CareerCluster"]
            .value_counts()
            .sort_index()
            .rename("Employees")
        )
        st.bar_chart(cluster_counts)

        if "Attrition" in filtered.columns:
            cluster_attrition = (
                filtered.assign(
                    AttritionFlag=(
                        filtered["Attrition"]
                        .astype(str)
                        .str.strip()
                        .eq("Yes")
                    ).astype(int)
                )
                .groupby("CareerCluster", observed=True)[
                    "AttritionFlag"
                ]
                .mean()
                .mul(100)
                .round(2)
                .rename("Attrition Rate (%)")
            )

            st.markdown("### Attrition Rate by Career Cluster")
            st.bar_chart(cluster_attrition)


# ============================================================
# TAB 5 — RISK & RETENTION
# ============================================================
with tab5:
    st.subheader("Risk & Retention")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Risk Level")
        if "PromotionGapRiskLevel" in filtered.columns:
            risk_counts = (
                filtered["PromotionGapRiskLevel"]
                .astype(str)
                .value_counts()
                .reindex(["Low", "Medium", "High"])
                .fillna(0)
                .astype(int)
            )
            st.bar_chart(risk_counts)

    with col2:
        st.markdown("### Retention Opportunity")
        if "RetentionOpportunityLevel" in filtered.columns:
            opportunity_counts = (
                filtered["RetentionOpportunityLevel"]
                .astype(str)
                .value_counts()
                .reindex(["Low", "Medium", "High"])
                .fillna(0)
                .astype(int)
            )
            st.bar_chart(opportunity_counts)

    if {"Department", "PromotionGapRiskLevel"}.issubset(
        filtered.columns
    ):
        dept_risk = (
            filtered.assign(
                HighRisk=(
                    filtered["PromotionGapRiskLevel"]
                    .astype(str)
                    .eq("High")
                ).astype(int)
            )
            .groupby("Department")["HighRisk"]
            .mean()
            .mul(100)
            .round(2)
            .rename("High Risk (%)")
            .sort_values()
        )

        st.markdown("### High Promotion Risk by Department")
        st.bar_chart(dept_risk)

    if {"PromotionGapRiskLevel", "Attrition"}.issubset(
        filtered.columns
    ):
        risk_attrition = (
            filtered.assign(
                AttritionFlag=(
                    filtered["Attrition"]
                    .astype(str)
                    .str.strip()
                    .eq("Yes")
                ).astype(int)
            )
            .groupby("PromotionGapRiskLevel", observed=True)[
                "AttritionFlag"
            ]
            .mean()
            .mul(100)
            .round(2)
            .reindex(["Low", "Medium", "High"])
            .rename("Attrition Rate (%)")
        )

        st.markdown("### Attrition Rate by Risk Level")
        st.bar_chart(risk_attrition)

    st.markdown("### Employee-Level Risk & Retention Output")

    output_cols = [
        c
        for c in [
            "EmployeeNumber",
            "Department",
            "JobRole",
            "JobLevel",
            "YearsAtCompany",
            "YearsInCurrentRole",
            "YearsSinceLastPromotion",
            "TrainingTimesLastYear",
            "CareerCluster",
            "PromotionGapRiskScore",
            "PromotionGapRiskLevel",
            "RetentionOpportunityScore",
            "RetentionOpportunityLevel",
            "RecommendedAction",
            "Attrition",
        ]
        if c in filtered.columns
    ]

    if output_cols:
        output_df = filtered[output_cols].copy()

        st.dataframe(
            output_df,
            use_container_width=True,
            height=420,
        )

        csv = output_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download filtered employee analysis",
            data=csv,
            file_name="filtered_hr_career_analysis.csv",
            mime="text/csv",
        )
    else:
        st.info("Employee-level risk fields are not available.")


# ============================================================
# FOOTER
# ============================================================
st.divider()

st.caption(
    "Decision-support dashboard. Risk and retention indicators are "
    "analytical signals, not proof that an employee will leave."
)
