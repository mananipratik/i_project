# HR Career Analytics Dashboard — Day 7

## Purpose

Interactive Streamlit dashboard for the HR career progression project.

## Dashboard Sections

1. Executive Overview
2. Workforce Analysis
3. Career Progression
4. Career Clusters
5. Risk & Retention

## Data

The dashboard looks for:

`data/hr_career_risk_analysis.csv`

If that file is unavailable, it falls back to:

`data/feature_engineered_palo_alto.csv`

## Run

From the project root:

```bash
streamlit run dashboard/app.py
```

## Important

Run the Day 5 and Day 6 notebooks before using Career Cluster and Risk/Retention pages.

The risk framework is decision-support only; it is not a validated prediction of employee attrition.
