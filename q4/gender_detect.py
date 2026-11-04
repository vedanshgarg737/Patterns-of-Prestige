"""Add a Gender column to the national awards data.

How it works (three layers, in this order of priority):

1. MANUAL OVERRIDES (gender_overrides.csv). Names that we checked by hand or by
   web search. These always win and are never touched by this script, so
   re-running it cannot undo a manual check.
2. HONORIFICS. A female honorific (Smt., Kum., Ms., Mrs., Begum, Mother, ...) in
   the first four words gives W. A male honorific as the first word (Shri, Sri,
   Shree, Mr) gives M.
3. EVERYTHING ELSE (bare "Dr.", "Prof.", "Pandit", military ranks, ...) is
   ambiguous. It is NOT guessed: Gender is left blank and the names are printed
   at the end of the run so that someone can check them.

To resolve a name that is printed as unresolved: add a row for it to
gender_overrides.csv (Name, Gender, Source) and run this script again.
Gender is M or W; use "Mixed" for a row that names two people of different
gender (a duo). Rows with a blank or "Mixed" gender are left out of the tests.

Run:  python gender_detect.py
"""

import os
import re
import sys

import pandas as pd

# ==========================================
# CONFIG
# ==========================================
INPUT_FILE = "national_awards_cleaned.csv"
NAME_COLUMN = "Name"
OVERRIDES_FILE = "gender_overrides.csv"  # columns: Name, Gender, Source (extra columns are ignored)
OUTPUT_FILE = "awards_with_gender.csv"

# ==========================================
# HONORIFIC PATTERNS
# ==========================================
FEMALE_PATTERNS = [
    r"\bsmt\.?\b",
    r"\bshrimati\b",
    r"\bsrimati\b",
    r"\bkum\.?\b",
    r"\bkumari\b",
    r"\bms\.?\b",
    r"\bmiss\.?\b",
    r"\bmrs\.?\b",
    r"\bbegum\b",
    r"\bbegam\b",
    r"\bbibi\b",
    r"\bsadhvi\b",
    r"\bsister\b",
    r"\bmata\b",
    r"\bmother\b",
    r"\bmaharani\b",
    r"\brajmata\b",
    r"\brajkumari\b",
    r"\bpandita\b",
    r"\bsushree\b",
    r"\blady\b",
    r"\bher\s+highness\b",
]
FEMALE_REGEX = re.compile("|".join(FEMALE_PATTERNS), re.IGNORECASE)
MALE_FIRST_WORDS = {"shri", "sri", "shree", "mr"}


def _tokens(name: str):
    # "Prof. Dr.(Smt.) Usha" -> ["Prof", "Dr", "Smt", "Usha"]
    return re.sub(r"[\(\)\[\]\.,]", " ", name.strip()).split()


def honorific_gender(name: str) -> str:
    """Return "W", "M" or "" (ambiguous) from the honorific alone."""
    if not isinstance(name, str) or not name.strip():
        return ""
    tokens = _tokens(name)
    if FEMALE_REGEX.search(" ".join(tokens[:4])):
        return "W"
    if tokens and tokens[0].lower() in MALE_FIRST_WORDS:
        return "M"
    return ""


def load_overrides(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    ov = pd.read_csv(path, dtype=str).fillna("")
    ov["Name"] = ov["Name"].str.strip()
    ov["Gender"] = ov["Gender"].str.strip()
    ov = ov[ov["Gender"].isin(["M", "W", "Mixed"])]
    return dict(zip(ov["Name"], ov["Gender"]))


def main() -> None:
    if not os.path.exists(INPUT_FILE):
        sys.exit(f"Error: could not find '{INPUT_FILE}' in this folder.")
    df = pd.read_csv(INPUT_FILE)
    if NAME_COLUMN not in df.columns:
        sys.exit(f"Error: column '{NAME_COLUMN}' not found. Columns: {list(df.columns)}")

    overrides = load_overrides(OVERRIDES_FILE)
    names = df[NAME_COLUMN].astype(str).str.strip()

    from_override = names.map(overrides)  # NaN when the name has no override
    from_honorific = names.map(honorific_gender)

    df["Gender"] = from_override.fillna(from_honorific)
    df["Gender_Source"] = "needs_review"
    df.loc[from_honorific.isin(["M", "W"]), "Gender_Source"] = "honorific"
    df.loc[from_override.notna(), "Gender_Source"] = "manual_check"

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved '{OUTPUT_FILE}' ({len(df)} rows).")
    print("\nGender by source:")
    print(pd.crosstab(df["Gender_Source"], df["Gender"].replace("", "(blank)")))

    unresolved = sorted(df.loc[df["Gender_Source"] == "needs_review", NAME_COLUMN].astype(str).unique())
    if unresolved:
        print(f"\n{len(unresolved)} names still need a gender (add them to '{OVERRIDES_FILE}'):")
        for n in unresolved:
            print("  -", n)
    else:
        print("\nAll names have a gender.")


if __name__ == "__main__":
    main()
