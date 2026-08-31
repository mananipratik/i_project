from pathlib import Path
import pandas as pd
import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="HR Career Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

FINAL_DATA = DATA_DIR / "hr_career_risk_analysis.csv"
FEATURE_DATA = DATA_DIR / "feature_engineered_palo_alto.csv"

# -----------------------------
# Helpers
# -----------------------------
@st.cache_data
def load_data():
    if FINAL_DATA.exists():
        data = pd.read_csv(FINAL_DATA)
        source = FINAL_DATA
    elif FEATURE_DATA.exists():
        data = pd.read_csv(FEATURE_DATA)
        source = FEATURE_DATA
    else:
        raise FileNotFoundError(
            "No analysis dataset found. Expected "
            "'data/hr_career_risk_analysis.csv' or "
            "'data/feature_engineered_palo_alto.csv'."
        )
    return data, source


def safe_rate(numerator, denominator):
    return (numerator / denominator * 100) if denominator else 0.0


def apply_filters(data):
    st.sidebar.header("🔎 Filters")

    filtered = data.copy()

    if "Department" in filtered.columns:
        departments = sorted(filtered["Department"].dropna().unique().tolist())
        selected_departments = st.sidebar.multiselect(
            "Department",
            departments,
            default=departments,
        )
        filtered = filtered[filtered["Department"].isin(selected_departments)]

    if "JobRole" in filtered.columns:
        roles = sorted(filtered["JobRole"].dropna().unique().tolist())
        selected_roles = st.sidebar.multiselect(
            "Job Role",
            roles,
            default=roles,
        )
        filtered = filtered[filtered["JobRole"].isin(selected_roles)]

    if "JobLevel" in filtered.columns:
        levels = sorted(filtered["JobLevel"].dropna().unique().tolist())
        selected_levels = st.sidebar.multiselect(
            "Job Level",
            levels,
            default=levels,
        )
        filtered = filtered[filtered["JobLevel"].isin(selected_levels)]

    if "CareerStage" in filtered.columns:
        stages = sorted(filtered["CareerStage"].dropna().astype(str).unique().tolist())
        selected_stages = st.sidebar.multiselect(
            "Career Stage",
            stages,
            default=stages,
        )
        filtered = filtered[filtered["CareerStage"].astype(str).isin(selected_stages)]

    if "CareerCluster" in filtered.columns:
        clusters = sorted(filtered["CareerCluster"].dropna().unique().tolist())
        selected_clusters = st.sidebar.multiselect(
            "Career Cluster",
            clusters,
            default=clusters,
        )
        filtered = filtered[filtered["CareerCluster"].isin(selected_clusters)]

    if "PromotionGapRiskLevel" in filtered.columns:
        risk_levels = ["Low", "Medium", "High"]
        available = [x for x in risk_levels if x in filtered["PromotionGapRiskLevel"].dropna().unique()]
        selected_risk = st.sidebar.multiselect(
            "Risk Level",
            available,
            default=available,
        )
        filtered = filtered[filtered["PromotionGapRiskLevel"].isin(selected_risk)]

    if "RetentionOpportunityLevel" in filtered.columns:
        opportunity_levels = ["Low", "Medium", "High"]
        available = [
            x for x in opportunity_levels
            if x in filtered["RetentionOpportunityLevel"].dropna().unique()
        ]
        selected_opportunity = st.sidebar.multiselect(
            "Retention Opportunity",
            available,
            default=available,
        )
        filtered = filtered[
            filtered["RetentionOpportunityLevel"].isin(selected_opportunity)
        ]

    return filtered


# -----------------------------
# Load
# -----------------------------
try:
    df, source_path = load_data()
except Exception as exc:
    st.error(str(exc))
    st.info(
        "Run the Day 6 notebook first and place the resulting CSV inside the "
        "project's data/ folder."
    )
    st.stop()

# -----------------------------
# Header
# -----------------------------
st.title("📊 HR Career Analytics Dashboard")
st.caption(
    "Career progression • promotion gaps • employee clustering • risk & retention opportunities"
)

st.sidebar.caption(f"Data source: {source_path.name}")

filtered = apply_filters(df)

if filtered.empty:
    st.warning("No employees match the selected filters. Adjust the filters in the sidebar.")
    st.stop()

# -----------------------------
# KPI row
# -----------------------------
total_employees = len(filtered)
attrition_rate = safe_rate((filtered["Attrition"] == "Yes").sum(), total_employees) if "Attrition" in filtered.columns else 0
avg_tenure = filtered["YearsAtCompany"].mean() if "YearsAtCompany" in filtered.columns else 0
high_risk = (filtered["PromotionGapRiskLevel"] == "High").sum() if "PromotionGapRiskLevel" in filtered.columns else 0
high_opportunity = (filtered["RetentionOpportunityLevel"] == "High").sum() if "RetentionOpportunityLevel" in filtered.columns else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Employees", f"{total_employees:,}")
c2.metric("Attrition Rate", f"{attrition_rate:.1f}%")
c3.metric("Avg. Years at Company", f"{avg_tenure:.1f}")
c4.metric("High Promotion Risk", f"{high_risk:,}")
c5.metric("High Retention Opportunity", f"{high_opportunity:,}")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏠 Executive Overview",
        "👥 Workforce Analysis",
        "📈 Career Progression",
        "🤖 Career Clusters",
        "🎯 Risk & Retention",
    ]
)

with tab1:
    st.subheader("Executive Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Employees by Department")
        if "Department" in filtered.columns:
            dept = filtered["Department"].value_counts().rename("Employees")
            st.bar_chart(dept)

    with col2:
        st.markdown("### Attrition")
        if "Attrition" in filtered.columns:
            attr = filtered["Attrition"].value_counts().rename("Employees")
            st.bar_chart(attr)

    st.markdown("### Promotion Risk")
    if "PromotionGapRiskLevel" in filtered.columns:
        risk = (
            filtered["PromotionGapRiskLevel"]
            .value_counts()
            .reindex(["Low", "Medium", "High"])
            .fillna(0)
            .astype(int)
        )
        st.bar_chart(risk)

with tab2:
    st.subheader("Workforce Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Job Role Distribution")
        if "JobRole" in filtered.columns:
            role = filtered["JobRole"].value_counts().sort_values()
            st.bar_chart(role)

    with col2:
        st.markdown("### Job Level Distribution")
        if "JobLevel" in filtered.columns:
            level = filtered["JobLevel"].value_counts().sort_index()
            st.bar_chart(level)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Age Distribution")
        if "Age" in filtered.columns:
            age_hist = (
                pd.cut(filtered["Age"], bins=10)
                .value_counts()
                .sort_index()
                .rename("Employees")
            )
            age_hist.index = age_hist.index.astype(str)
            st.bar_chart(age_hist)

    with col4:
        st.markdown("### Career Stage")
        if "CareerStage" in filtered.columns:
            stage = filtered["CareerStage"].astype(str).value_counts()
            st.bar_chart(stage)

with tab3:
    st.subheader("Career Progression")

    metric_cols = st.columns(4)

    progression_metrics = [
        ("Avg. Years at Company", "YearsAtCompany"),
        ("Avg. Years in Current Role", "YearsInCurrentRole"),
        ("Avg. Years Since Promotion", "YearsSinceLastPromotion"),
        ("Avg. Years with Current Manager", "YearsWithCurrManager"),
    ]

    for container, (label, col) in zip(metric_cols, progression_metrics):
        value = filtered[col].mean() if col in filtered.columns else 0
        container.metric(label, f"{value:.1f}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Average Promotion Gap by Department")
        if {"Department", "YearsSinceLastPromotion"}.issubset(filtered.columns):
            promotion = (
                filtered.groupby("Department")["YearsSinceLastPromotion"]
                .mean()
                .sort_values()
            )
            st.bar_chart(promotion)

    with col2:
        st.markdown("### Average Time in Current Role by Department")
        if {"Department", "YearsInCurrentRole"}.issubset(filtered.columns):
            role_time = (
                filtered.groupby("Department")["YearsInCurrentRole"]
                .mean()
                .sort_values()
            )
            st.bar_chart(role_time)

    st.markdown("### Promotion Gap Groups")
    if "PromotionGapGroup" in filtered.columns:
        gap_group = filtered["PromotionGapGroup"].astype(str).value_counts()
        st.bar_chart(gap_group)

    st.markdown("### Career Progression Data")
    progression_cols = [
        c for c in [
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
    st.dataframe(filtered[progression_cols], use_container_width=True)

with tab4:
    st.subheader("Career Clusters")

    if "CareerCluster" not in filtered.columns:
        st.info(
            "CareerCluster is not present in the loaded dataset. "
            "Run Day 5 clustering and save the cluster labels before using this page."
        )
    else:
        cluster_summary = (
            filtered.groupby("CareerCluster")
            .agg(
                Employees=("CareerCluster", "size"),
                Avg_YearsAtCompany=("YearsAtCompany", "mean"),
                Avg_YearsInCurrentRole=("YearsInCurrentRole", "mean"),
                Avg_YearsSinceLastPromotion=("YearsSinceLastPromotion", "mean"),
                Avg_JobLevel=("JobLevel", "mean"),
            )
            .round(2)
        )
        st.dataframe(cluster_summary, use_container_width=True)

        st.markdown("### Employees by Career Cluster")
        st.bar_chart(
            filtered["CareerCluster"].value_counts().sort_index().rename("Employees")
        )

        if "Attrition" in filtered.columns:
            cluster_attrition = (
                filtered.assign(
                    AttritionFlag=(filtered["Attrition"] == "Yes").astype(int)
                )
                .groupby("CareerCluster")["AttritionFlag"]
                .mean()
                .mul(100)
                .round(2)
                .rename("Attrition Rate (%)")
            )
            st.markdown("### Attrition Rate by Career Cluster")
            st.bar_chart(cluster_attrition)

with tab5:
    st.subheader("Risk & Retention")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Risk Level")
        if "PromotionGapRiskLevel" in filtered.columns:
            risk_counts = (
                filtered["PromotionGapRiskLevel"]
                .value_counts()
                .reindex(["Low", "Medium", "High"])
                .fillna(0)
            )
            st.bar_chart(risk_counts)

    with col2:
        st.markdown("### Retention Opportunity")
        if "RetentionOpportunityLevel" in filtered.columns:
            opportunity_counts = (
                filtered["RetentionOpportunityLevel"]
                .value_counts()
                .reindex(["Low", "Medium", "High"])
                .fillna(0)
            )
            st.bar_chart(opportunity_counts)

    if {"Department", "PromotionGapRiskLevel"}.issubset(filtered.columns):
        dept_risk = (
            filtered.assign(
                HighRisk=(filtered["PromotionGapRiskLevel"] == "High").astype(int)
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

    if {"PromotionGapRiskLevel", "Attrition"}.issubset(filtered.columns):
        risk_attrition = (
            filtered.assign(
                AttritionFlag=(filtered["Attrition"] == "Yes").astype(int)
            )
            .groupby("PromotionGapRiskLevel")["AttritionFlag"]
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
        c for c in [
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

    output_df = filtered[output_cols].copy()
    st.dataframe(output_df, use_container_width=True, height=420)

    csv = output_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered employee analysis",
        data=csv,
        file_name="filtered_hr_career_analysis.csv",
        mime="text/csv",
    )

st.divider()
st.caption(
    "Decision-support dashboard. Risk and retention indicators are analytical signals, "
    "not proof that an employee will leave."
)
