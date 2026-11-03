"""
Q1 (region part): How has the regional distribution of civilian award winners
changed between the first 40 years and the later years?

Steps
  1. Load the cleaned civilian awards CSV.
  2. Map every State/Country to a broad region (North, South, East, West,
     Central, North-East, Foreign).
  3. Split winners into two periods (PERIOD_1 and PERIOD_2).
  4. For each award write CSVs (zone level + state level), sorted region-wise.
  5. Make Plotly charts (saved as interactive HTML).
  6. Run a chi-square test on zone counts (H0: region distribution unchanged).

Run:  python region_analysis.py
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
INPUT_CSV = "../datasets/cleaned_datasets/national_awards_cleaned.csv"
OUT_DIR = "region_output"

# Data runs 1954-2021 (68 years). "First 40 years" = 1954-1993, "next" = 1994-2021.
# NOTE: the period 2 has only 28 years of data, so shares (%) are used for
# comparison as well as raw counts. If your report means the *latest* 40 years
# (1982-2021), change PERIOD_2 to (1982, 2021) - the two periods will overlap.
PERIOD_1 = (1954, 1993)
PERIOD_2 = (1994, 2021)

AWARDS = ["Bharat Ratna", "Padma Vibhushan", "Padma Bhushan", "Padma Shri"]

# ----------------------------------------------------------------------------
# State/Country -> Region
# ----------------------------------------------------------------------------
REGION_MAP = {
    # North
    "Delhi": "North", "Punjab": "North", "Haryana": "North", "Chandigarh": "North",
    "Himachal Pradesh": "North", "Jammu and Kashmir": "North", "Ladakh": "North",
    "Uttarakhand": "North", "Uttar Pradesh": "North", "Rajasthan": "North",
    # South
    "Tamil Nadu": "South", "Karnataka": "South", "Kerala": "South",
    "Telangana": "South", "Andhra Pradesh": "South", "Puducherry": "South",
    "Lakshadweep": "South",
    # East
    "West Bengal": "East", "Odisha": "East", "Bihar": "East", "Jharkhand": "East",
    "Andaman and Nicobar": "East",
    # West
    "Maharashtra": "West", "Gujarat": "West", "Goa": "West", "Daman and Diu": "West",
    # Central
    "Madhya Pradesh": "Central", "Chhattisgarh": "Central",
    # North-East
    "Assam": "North-East", "Manipur": "North-East", "Mizoram": "North-East",
    "Meghalaya": "North-East", "Sikkim": "North-East", "Nagaland": "North-East",
    "Arunachal Pradesh": "North-East", "Tripura": "North-East",
}
REGION_ORDER = ["North", "South", "East", "West", "Central", "North-East", "Foreign"]


def to_region(place: str) -> str:
    # anything not an Indian state/UT in the map is a foreign country
    return REGION_MAP.get(place, "Foreign")


def assign_period(year: int) -> str | None:
    if PERIOD_1[0] <= year <= PERIOD_1[1]:
        return f"{PERIOD_1[0]}-{PERIOD_1[1]}"
    if PERIOD_2[0] <= year <= PERIOD_2[1]:
        return f"{PERIOD_2[0]}-{PERIOD_2[1]}"
    return None


P1_LABEL = f"{PERIOD_1[0]}-{PERIOD_1[1]}"
P2_LABEL = f"{PERIOD_2[0]}-{PERIOD_2[1]}"


# ----------------------------------------------------------------------------
# Load + prepare
# ----------------------------------------------------------------------------
def load_data() -> pd.DataFrame:
    df = pd.read_csv(INPUT_CSV)
    df.columns = df.columns.str.strip()
    df["State/Country"] = df["State/Country"].astype(str).str.strip()
    df["Award"] = df["Award"].astype(str).str.strip()
    df["Region"] = df["State/Country"].map(to_region)
    df["Period"] = df["Year"].apply(assign_period)
    df = df.dropna(subset=["Period"])
    return df


def slug(name: str) -> str:
    return name.lower().replace(" ", "_")


# ----------------------------------------------------------------------------
# Summaries -> CSV
# ----------------------------------------------------------------------------
def region_summary(sub: pd.DataFrame) -> pd.DataFrame:
    """Zone-level counts and % share for each period, sorted region-wise."""
    out = (sub.groupby(["Period", "Region"]).size().reset_index(name="Count"))
    # make sure every region/period pair exists (fill 0)
    full = pd.MultiIndex.from_product([[P1_LABEL, P2_LABEL], REGION_ORDER],
                                      names=["Period", "Region"])
    out = out.set_index(["Period", "Region"]).reindex(full, fill_value=0).reset_index()
    out["Share_%"] = (out["Count"] / out.groupby("Period")["Count"].transform("sum") * 100).round(2)
    out["Region"] = pd.Categorical(out["Region"], REGION_ORDER, ordered=True)
    out["Period"] = pd.Categorical(out["Period"], [P1_LABEL, P2_LABEL], ordered=True)
    return out.sort_values(["Period", "Region"]).reset_index(drop=True)


def state_summary(sub: pd.DataFrame) -> pd.DataFrame:
    """State-level counts, grouped by region, sorted by count within region."""
    out = (sub.groupby(["Period", "Region", "State/Country"]).size().reset_index(name="Count"))
    out["Share_%"] = (out["Count"] / out.groupby("Period")["Count"].transform("sum") * 100).round(2)
    out["Region"] = pd.Categorical(out["Region"], REGION_ORDER, ordered=True)
    out["Period"] = pd.Categorical(out["Period"], [P1_LABEL, P2_LABEL], ordered=True)
    return out.sort_values(["Period", "Region", "Count"],
                           ascending=[True, True, False]).reset_index(drop=True)


# ----------------------------------------------------------------------------
# Plots
# ----------------------------------------------------------------------------
def plot_region_share(reg: pd.DataFrame, award: str, path: str):
    fig = px.bar(reg, x="Region", y="Share_%", color="Period", barmode="group",
                 text="Count", category_orders={"Region": REGION_ORDER},
                 title=f"{award}: regional share of winners ({P1_LABEL} vs {P2_LABEL})",
                 labels={"Share_%": "Share of winners in period (%)"})
    fig.update_traces(textposition="outside")
    fig.write_html(path)
    return fig


def plot_top_states(st: pd.DataFrame, award: str, path: str, n: int = 10):
    top = st.groupby("State/Country")["Count"].sum().nlargest(n).index
    d = st[st["State/Country"].isin(top)]
    fig = px.bar(d, x="State/Country", y="Share_%", color="Period", barmode="group",
                 category_orders={"State/Country": list(top)},
                 title=f"{award}: top {n} states/countries ({P1_LABEL} vs {P2_LABEL})",
                 labels={"Share_%": "Share of winners in period (%)"})
    fig.write_html(path)
    return fig


def plot_overview(all_reg: pd.DataFrame, path: str):
    """One panel per award, zone share by period."""
    awards = list(all_reg["Award"].unique())
    fig = make_subplots(rows=2, cols=2, subplot_titles=awards)
    colors = {P1_LABEL: "#1f77b4", P2_LABEL: "#ff7f0e"}
    for i, award in enumerate(awards):
        r, c = divmod(i, 2)
        for p in (P1_LABEL, P2_LABEL):
            d = all_reg[(all_reg["Award"] == award) & (all_reg["Period"] == p)]
            fig.add_trace(go.Bar(x=d["Region"], y=d["Share_%"], name=p,
                                 marker_color=colors[p], legendgroup=p,
                                 showlegend=(i == 0)), row=r + 1, col=c + 1)
    fig.update_layout(barmode="group", height=750,
                      title="Regional share of civilian award winners by award")
    fig.update_yaxes(title_text="Share (%)")
    fig.write_html(path)
    return fig


def plot_heatmap(df: pd.DataFrame, path: str):
    """All Padma/Bharat Ratna winners: region x 5-year bin (counts as %)."""
    d = df.copy()
    d["Bin"] = (d["Year"] // 5 * 5).astype(str)
    piv = d.groupby(["Bin", "Region"]).size().unstack(fill_value=0).reindex(columns=REGION_ORDER, fill_value=0)
    piv = piv.div(piv.sum(axis=1), axis=0) * 100
    fig = px.imshow(piv.T.round(1), text_auto=True, aspect="auto", color_continuous_scale="Blues",
                    labels=dict(x="5-year bin (start)", y="Region", color="% of winners"),
                    title="Regional share of all civilian winners over time (5-year bins)")
    fig.write_html(path)
    return fig


# ----------------------------------------------------------------------------
# Chi-square test (H0: region distribution is the same in both periods)
# ----------------------------------------------------------------------------
def chi_square(sub: pd.DataFrame, award: str):
    from scipy.stats import chi2_contingency
    tab = pd.crosstab(sub["Period"], sub["Region"])
    tab = tab.loc[:, tab.sum() > 0]
    chi2, p, dof, exp = chi2_contingency(tab)
    low = (exp < 5).sum() / exp.size
    note = "" if low <= 0.2 else "  (WARNING: many expected counts < 5, result unreliable)"
    print(f"{award:16s} chi2={chi2:8.2f}  dof={dof}  p={p:.4g}{note}")
    return {"Award": award, "chi2": round(chi2, 3), "dof": dof, "p_value": p,
            "reliable": low <= 0.2}


# ----------------------------------------------------------------------------
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = load_data()
    print(f"Rows used: {len(df)}  ({P1_LABEL}: {(df.Period == P1_LABEL).sum()}, "
          f"{P2_LABEL}: {(df.Period == P2_LABEL).sum()})")

    all_reg, tests = [], []
    for award in AWARDS:
        sub = df[df["Award"] == award]
        if sub.empty:
            continue
        reg, st = region_summary(sub), state_summary(sub)

        reg.to_csv(f"{OUT_DIR}/{slug(award)}_region_summary.csv", index=False)
        st.to_csv(f"{OUT_DIR}/{slug(award)}_state_summary.csv", index=False)

        plot_region_share(reg, award, f"{OUT_DIR}/{slug(award)}_region_share.html")
        plot_top_states(st, award, f"{OUT_DIR}/{slug(award)}_top_states.html")

        reg = reg.assign(Award=award)
        all_reg.append(reg)
        tests.append(chi_square(sub, award))

    plot_overview(pd.concat(all_reg), f"{OUT_DIR}/overview_all_awards.html")
    plot_heatmap(df, f"{OUT_DIR}/region_heatmap_over_time.html")
    pd.DataFrame(tests).to_csv(f"{OUT_DIR}/chi_square_results.csv", index=False)
    print(f"Done. Files saved in ./{OUT_DIR}/")


if __name__ == "__main__":
    main()
