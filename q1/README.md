# Q1: Region and Age of Civilian Award Winners
Team 007 | An Analysis of India's Civilian and Military Honours

Compares civilian award winners (Bharat Ratna and Padma awards) in 1954-1993 vs 1994-2021.

## Setup
    pip install -r requirements.txt

## Files
| File | Purpose |
|---|---|
| national_awards_cleaned.csv | Input data (cleaned civilian awards) |
| region_analysis.py / .ipynb | Maps states to regions, writes region CSVs to region_output/, makes charts, chi-square test per award |
| age_analysis.py / .ipynb | Writes age CSVs to age_output/, makes age charts |
| H0_analysis.ipynb ... H3_analysis.ipynb | One notebook per hypothesis: reads the CSVs, tests region (chi-square) and age (Mann-Whitney), plots, and gives a verdict. Outputs go to hypothesis_output/ |

## Run order
1. region_analysis.ipynb (or `python region_analysis.py`)
2. age_analysis.ipynb (or `python age_analysis.py`) - needs region_analysis.py in the same folder
3. H0_analysis.ipynb, H1_analysis.ipynb, H2_analysis.ipynb, H3_analysis.ipynb

The H notebooks run steps 1 and 2 automatically if region_output/ or age_output/ is missing.

## Settings
Periods are set at the top of region_analysis.py (PERIOD_1, PERIOD_2). The region grouping is REGION_MAP in the same file.

## Result
Region (p ~ 8e-27) and age (p ~ 2e-17) both changed significantly, so H3 is supported and H0, H1, H2 are rejected.

## Caveat
Only winners with a known birth year have an age (1,650 of 4,875). For 1994-2021, ages exist only for 1997-2009. See age_output/age_coverage_by_year.csv.
