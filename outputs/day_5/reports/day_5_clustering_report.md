# Day 5 — Career Path Clustering Report

Input dataset: ../data/feature_engineered/Palo Alto Networks_feature_engineered.csv

Rows: 1470

Clustering features: 10

Selected K: 4

## Methods
- StandardScaler
- K-Means
- Elbow Method
- Silhouette Score
- PCA visualization
- Hierarchical / Agglomerative Clustering

## Validation
K-Means silhouette score: 0.2275

Hierarchical silhouette score: 0.1795

## Interpretation
Highest PromotionGapRatio cluster: 2

Highest RoleStagnationRatio cluster: 2

Highest attrition-rate cluster: 1

Largest cluster: 3

Highest descriptive stagnation-signal cluster: 2

## Important Note
Clusters are created without Attrition. Attrition is compared after clustering. A high stagnation signal is not proof that an employee is dissatisfied or will leave.
