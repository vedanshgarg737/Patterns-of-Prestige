"""
Q1 (age part): generates the age CSVs used by the H1 / H2 / H3 notebooks.

Uses the same periods, awards and region mapping as region_analysis.py
(this file imports them, so change PERIOD_1 / PERIOD_2 there only).

Outputs (in age_output/):
  age_records.csv              one row per winner that HAS an age
  <award>_age_summary.csv      n, mean, median, std, quartiles per period
  all_civilian_age_summary.csv same, all awards pooled
  age_bins.csv                 count and % per 10-year age band, per award/period
  age_coverage_by_year.csv     how many winners have an age, by year (data quality)

Run:  python age_analysis.py
"""

import os
import pandas as pd

from region_analysis import (AWARDS, PERIOD_1, PERIOD_2, P1_LABEL, P2_LABEL,
                             load_data, slug)

OUT_DIR = "age_output"
BINS = [0, 40, 50, 60, 70, 80, 200]
BIN_LABELS = ["<40", "40-49", "50-59", "60-69", "70-79", "80+"]


def describe(d: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for period in (P1_LABEL, P2_LABEL):
        a = d.loc[d["Period"] == period, "AgeAtAward"]
        rows.append({
            "Period": period, "n": len(a),
            "mean": round(a.mean(), 2), "median": a.median(),
            "std": round(a.std(), 2), "min": a.min(),
            "q1": a.quantile(0.25), "q3": a.quantile(0.75), "max": a.max(),
        })
    return pd.DataFrame(rows)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = load_data()                       # already has Region + Period columns
    total_per_year = df.groupby("Year").size()

    aged = df.dropna(subset=["AgeAtAward"]).copy()
    print(f"Winners with an age: {len(aged)} of {len(df)}")
    print(aged.groupby(["Award", "Period"]).size().unstack(fill_value=0))

    cols = ["Name", "Award", "Field", "State/Country", "Region", "Year",
            "Year of Birth", "AgeAtAward", "Period"]
    aged[cols].sort_values(["Period", "Award", "Year"]).to_csv(
        f"{OUT_DIR}/age_records.csv", index=False)

    # summaries
    for award in AWARDS:
        sub = aged[aged["Award"] == award]
        if sub.empty:
            continue
        describe(sub).to_csv(f"{OUT_DIR}/{slug(award)}_age_summary.csv", index=False)
    describe(aged).to_csv(f"{OUT_DIR}/all_civilian_age_summary.csv", index=False)

    # age bands (per award + pooled)
    aged["AgeBand"] = pd.cut(aged["AgeAtAward"], BINS, labels=BIN_LABELS, right=False)
    parts = []
    for award, sub in list(aged.groupby("Award")) + [("All awards", aged)]:
        t = (sub.groupby(["Period", "AgeBand"], observed=False).size()
                .reset_index(name="Count"))
        t["Share_%"] = (t["Count"] / t.groupby("Period")["Count"].transform("sum") * 100).round(2)
        t.insert(0, "Award", award)
        parts.append(t)
    pd.concat(parts).to_csv(f"{OUT_DIR}/age_bins.csv", index=False)

    # coverage by year (data quality)
    cov = pd.DataFrame({"Total_records": total_per_year,
                        "With_age": aged.groupby("Year").size()}).fillna(0).astype(int)
    cov["Coverage_%"] = (cov["With_age"] / cov["Total_records"] * 100).round(1)
    cov.reset_index().to_csv(f"{OUT_DIR}/age_coverage_by_year.csv", index=False)

    print(f"Done. Files saved in ./{OUT_DIR}/")


if __name__ == "__main__":
    main()
