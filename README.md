# 📊 HR Career Analytics — Career Progression & Promotion Gap Analysis

## 📌 Project Overview

This project is an end-to-end **HR Analytics / Data Science project** focused on understanding employee career progression, promotion gaps, role stagnation, career-path patterns, and retention opportunities.

Instead of focusing only on the question:

> **"Who might leave the organization?"**

this project also investigates:

> **"Which employees or workforce groups may be experiencing career progression challenges?"**

The project uses Python-based data analysis, feature engineering, unsupervised learning, risk analysis, and an interactive Streamlit dashboard to provide HR-oriented insights.

---

# 🎯 Business Problem

Traditional employee attrition analysis mainly focuses on identifying employees who may leave.

However, employee retention can also be influenced by factors such as:

- Long promotion gaps
- Long periods in the same role
- Limited career progression
- Training and development opportunities
- Managerial stability
- Career-path patterns

Therefore, this project analyzes career progression data to identify potential career stagnation and provide proactive HR decision-support insights.

---

# 🎯 Project Objectives

The main objectives of this project are:

1. Understand the employee workforce structure.
2. Perform data validation and cleaning.
3. Analyze employee career progression.
4. Analyze promotion gaps.
5. Identify role-stagnation patterns.
6. Create career-related engineered features.
7. Segment employees using clustering.
8. Develop an explainable promotion-gap risk score.
9. Identify retention opportunities.
10. Provide recommended HR actions.
11. Build an interactive HR Analytics dashboard.
12. Provide data-driven insights for HR decision-making.

---

# 📂 Dataset

### Dataset Name

`Palo Alto Networks.csv`

The dataset contains employee-level HR information related to:

- Employee demographics
- Department
- Job role
- Job level
- Compensation
- Job satisfaction
- Performance
- Training
- Tenure
- Promotion history
- Manager relationship
- Attrition

### Important Variables

| Variable | Description |
|---|---|
| `Age` | Employee age |
| `Attrition` | Employee attrition status |
| `Department` | Employee department |
| `JobRole` | Employee job role |
| `JobLevel` | Employee seniority level |
| `YearsAtCompany` | Years spent at the company |
| `YearsInCurrentRole` | Years spent in current role |
| `YearsSinceLastPromotion` | Years since last promotion |
| `YearsWithCurrManager` | Years with current manager |
| `TrainingTimesLastYear` | Training sessions completed last year |
| `PerformanceRating` | Employee performance rating |
| `JobSatisfaction` | Employee job satisfaction |

---

# 📁 project structure
i_project/
│
├── .devcontainer/
│
├── dashboard/
│   └── dashboard/
│       ├── ...
│       ├── outputs/
│       ├── README_DAY7.md
│       └── requirements.txt
│
├── data/
│   ├── cleaned/
│   ├── clustering/
│   ├── feature_engineered/
│   ├── Palo Alto Networks.csv
│   ├── feature_engineered_palo_alto.csv
│   └── hr_career_risk_analysis.csv
│
├── nb/
│   ├── ...
│   └── your Day 1–6 notebooks
│
├── outputs/
│   ├── ...
│   └── reports / tables / figures
│
├── .gitattributes
├── README.md
└── requirements.txt

---

# 🧠 Data Science Workflow

The complete project follows this workflow:

```text
Raw Dataset
     ↓
Business Understanding
     ↓
Data Validation & Cleaning
     ↓
Exploratory Data Analysis
     ↓
Feature Engineering
     ↓
Career Path Clustering
     ↓
Promotion Gap Risk Analysis
     ↓
Retention Opportunity Analysis
     ↓
Streamlit Dashboard
     ↓
Business Recommendations

