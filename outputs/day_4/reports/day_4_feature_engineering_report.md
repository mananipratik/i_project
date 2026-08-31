# Day 4 — Feature Engineering Report

## Input
../data/cleaned/Palo Alto Networks_cleaned.csv

## Dataset Shape
(1470, 38)

## Engineered Features
- PromotionGapRatio
- RoleStagnationRatio
- ManagerStabilityRatio
- CareerStage
- PromotionGapGroup
- RoleDurationGroup
- TrainingGroup

## Validation
- Missing values in engineered features: 0
- Infinite ratio values: 0
- Negative ratio values: 0

## Important Note
Ratio values above 1 are reported for investigation because Day 2 documented logical career-duration inconsistencies.

## Output
Feature-engineered dataset:
../data/feature_engineered/Palo Alto Networks_feature_engineered.csv

Tables:
../outputs/day_4/tables
