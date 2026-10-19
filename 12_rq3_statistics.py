
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# FILE PATHS
# ==========================================================

RESULT_FILE = "data/rejection_reasons.json"

OUTPUT_DIR = Path("results/rq3")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# LOAD RESULTS
# ==========================================================

with open(
    RESULT_FILE,
    encoding="utf8"
) as f:

    prs = json.load(f)


# ==========================================================
# CREATE DATAFRAME
# ==========================================================

data = []

for pr in prs:

    data.append({

        "repo": pr["repo"],

        "rejection_reason": pr["rejection_reason"]["value"]

    })

df = pd.DataFrame(data)


# ==========================================================
# CALCULATE STATISTICS
# ==========================================================

summary = (

    df["rejection_reason"]

    .value_counts()

    .rename_axis("Rejection Reason")

    .reset_index(name="Count")

)

summary["Percentage"] = (

    summary["Count"]

    / summary["Count"].sum()

    * 100

).round(2)


# ==========================================================
# EXPORT CSV
# ==========================================================

CSV_FILE = OUTPUT_DIR / "rejection_reason.csv"

summary.to_csv(
    CSV_FILE,
    index=False,
    encoding="utf8"
)


# ==========================================================
# EXPORT EXCEL
# ==========================================================

XLSX_FILE = OUTPUT_DIR / "rejection_reason.xlsx"

summary.to_excel(
    XLSX_FILE,
    index=False
)


# ==========================================================
# GENERATE PER-PROJECT SUMMARY
# ==========================================================

PROJECT_FILE = OUTPUT_DIR / "rq3_by_project.xlsx"

project_summary = pd.crosstab(
    df["repo"],
    df["rejection_reason"]
)

project_summary.to_excel(
    PROJECT_FILE
)


# ==========================================================
# GENERATE BAR CHART
# ==========================================================

BAR_FILE = OUTPUT_DIR / "rejection_reason_bar.png"

plt.figure(figsize=(9, 5))

bars = plt.bar(
    summary["Rejection Reason"],
    summary["Count"]
)

plt.title(
    "RQ3 - Rejection Reasons"
)

plt.xlabel(
    "Rejection Reason"
)

plt.ylabel(
    "Number of PRs"
)

plt.xticks(rotation=20)

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        str(int(height)),
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    BAR_FILE,
    dpi=300
)

plt.close()


# ==========================================================
# GENERATE PIE CHART
# ==========================================================

PIE_FILE = OUTPUT_DIR / "rejection_reason_pie.png"

plt.figure(figsize=(7, 7))

plt.pie(
    summary["Count"],
    labels=summary["Rejection Reason"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "RQ3 - Rejection Reasons"
)

plt.tight_layout()

plt.savefig(
    PIE_FILE,
    dpi=300
)

plt.close()


# ==========================================================
# GENERATE TEXT SUMMARY
# ==========================================================

TXT_FILE = OUTPUT_DIR / "rq3_results.txt"

total = summary["Count"].sum()

most_frequent = summary.iloc[0]

with open(
    TXT_FILE,
    "w",
    encoding="utf8"
) as f:

    f.write("=" * 60 + "\n")

    f.write("RQ3\n")

    f.write("=" * 60 + "\n\n")

    f.write(
        "Research Question:\n"
    )

    f.write(
        "What are the primary reasons that suggestions for resolving Technical Debt issues are rejected?\n\n"
    )

    f.write(
        f"Total rejected PRs analyzed: {total}\n\n"
    )

    f.write(
        "Distribution of rejection reasons:\n\n"
    )

    for _, row in summary.iterrows():

        f.write(
            f"{row['Rejection Reason']}: "
            f"{row['Count']} "
            f"({row['Percentage']:.2f}%)\n"
        )

    f.write("\n")

    f.write(
        "Most frequent rejection reason:\n"
    )

    f.write(
        f"{most_frequent['Rejection Reason']} "
        f"({most_frequent['Count']} PRs - "
        f"{most_frequent['Percentage']:.2f}%)\n"
    )


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print()

print("=" * 70)

print("RQ3")

print("=" * 70)

print()

print(summary)

print()

print(f"Total rejected PRs: {total}")

print()

print("Most frequent rejection reason:")

print(
    f"{most_frequent['Rejection Reason']} "
    f"({most_frequent['Count']} PRs - "
    f"{most_frequent['Percentage']:.2f}%)"
)

print()

print("=" * 70)

print("GENERATED FILES")

print("=" * 70)

print()

print(f"CSV   : {CSV_FILE}")

print(f"Excel : {XLSX_FILE}")

print(f"Bar   : {BAR_FILE}")

print(f"Pie   : {PIE_FILE}")

print(f"Text  : {TXT_FILE}")

print(f"Project summary: {PROJECT_FILE}")

print()

print(f"Directory: {OUTPUT_DIR}")

print()

print("=" * 70)
