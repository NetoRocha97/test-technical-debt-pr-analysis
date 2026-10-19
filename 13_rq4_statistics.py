
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# FILE PATHS
# ==========================================================

RESULT_FILE = "data/llm_results_final.json"

OUTPUT_DIR = Path("results/rq4")

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

        "test_td_mentioned": pr["test_td_mentioned"]["value"],

        "mention_type": pr["mention_type"]["value"],

        "test_td_type": pr["test_td_type"]["value"],

        "agreement": pr["agreement"]["value"],

        "resolution": pr["resolution"]["value"]

    })

df = pd.DataFrame(data)


# ==========================================================
# STATISTICAL FUNCTIONS
# ==========================================================

def generate_summary(column):

    summary = (

        df[column]

        .value_counts()

        .rename_axis(column)

        .reset_index(name="Count")

    )

    summary["Percentage"] = (

        summary["Count"]

        / summary["Count"].sum()

        * 100

    ).round(2)

    return summary


def save_table(summary, name):

    csv_file = OUTPUT_DIR / f"{name}.csv"

    xlsx_file = OUTPUT_DIR / f"{name}.xlsx"

    summary.to_csv(
        csv_file,
        index=False,
        encoding="utf8"
    )

    summary.to_excel(
        xlsx_file,
        index=False
    )

    return csv_file, xlsx_file


# ==========================================================
# GENERATE CHARTS
# ==========================================================

def generate_charts(summary, title, name):

    plt.figure(figsize=(9, 5))

    bars = plt.bar(
        summary.iloc[:, 0],
        summary["Count"]
    )

    plt.title(title)

    plt.xlabel("Category")

    plt.ylabel("Number of PRs")

    plt.xticks(rotation=25)

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
        OUTPUT_DIR / f"{name}_bar.png",
        dpi=300
    )

    plt.close()

    plt.figure(figsize=(7, 7))

    plt.pie(
        summary["Count"],
        labels=summary.iloc[:, 0],
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(title)

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / f"{name}_pie.png",
        dpi=300
    )

    plt.close()


# ==========================================================
# MAIN STATISTICS
# ==========================================================

summary_mentioned = generate_summary(
    "test_td_mentioned"
)

summary_mention_type = generate_summary(
    "mention_type"
)

summary_td_type = generate_summary(
    "test_td_type"
)

save_table(
    summary_mentioned,
    "test_td_mentioned"
)

save_table(
    summary_mention_type,
    "mention_type"
)

save_table(
    summary_td_type,
    "test_td_type"
)

generate_charts(
    summary_mentioned,
    "RQ4 - Test TD Mentioned",
    "test_td_mentioned"
)

generate_charts(
    summary_mention_type,
    "RQ4 - Mention Type",
    "mention_type"
)

generate_charts(
    summary_td_type,
    "RQ4 - Test TD Type",
    "test_td_type"
)


# ==========================================================
# HOW ARE TEST TDs ADDRESSED?
# ==========================================================

agreement_by_td = pd.crosstab(
    df["test_td_type"],
    df["agreement"],
    margins=True
)

resolution_by_td = pd.crosstab(
    df["test_td_type"],
    df["resolution"],
    margins=True
)

agreement_file = OUTPUT_DIR / "agreement_by_td_type.xlsx"

resolution_file = OUTPUT_DIR / "resolution_by_td_type.xlsx"

agreement_by_td.to_excel(
    agreement_file
)

resolution_by_td.to_excel(
    resolution_file
)


# ==========================================================
# ROW-WISE PERCENTAGES
# ==========================================================

agreement_percentage = (

    pd.crosstab(
        df["test_td_type"],
        df["agreement"],
        normalize="index"
    )

    * 100

).round(2)

resolution_percentage = (

    pd.crosstab(
        df["test_td_type"],
        df["resolution"],
        normalize="index"
    )

    * 100

).round(2)

agreement_percentage_file = (
    OUTPUT_DIR /
    "agreement_by_td_type_percentage.xlsx"
)

resolution_percentage_file = (
    OUTPUT_DIR /
    "resolution_by_td_type_percentage.xlsx"
)

agreement_percentage.to_excel(
    agreement_percentage_file
)

resolution_percentage.to_excel(
    resolution_percentage_file
)


# ==========================================================
# PER-PROJECT STATISTICS
# ==========================================================

PROJECT_FILE = OUTPUT_DIR / "rq4_by_project.xlsx"

with pd.ExcelWriter(
    PROJECT_FILE,
    engine="openpyxl"
) as writer:

    pd.crosstab(
        df["repo"],
        df["test_td_mentioned"]
    ).to_excel(
        writer,
        sheet_name="test_td_mentioned"
    )

    pd.crosstab(
        df["repo"],
        df["mention_type"]
    ).to_excel(
        writer,
        sheet_name="mention_type"
    )

    pd.crosstab(
        df["repo"],
        df["test_td_type"]
    ).to_excel(
        writer,
        sheet_name="test_td_type"
    )

    agreement_by_td.to_excel(
        writer,
        sheet_name="agreement_by_type"
    )

    resolution_by_td.to_excel(
        writer,
        sheet_name="resolution_by_type"
    )

    agreement_percentage.to_excel(
        writer,
        sheet_name="agreement_%"
    )

    resolution_percentage.to_excel(
        writer,
        sheet_name="resolution_%"
    )


# ==========================================================
# GENERATE TEXT REPORT
# ==========================================================

TXT_FILE = OUTPUT_DIR / "rq4_results.txt"

with open(
    TXT_FILE,
    "w",
    encoding="utf8"
) as f:

    f.write("=" * 70 + "\n")

    f.write("RQ4\n")

    f.write("=" * 70 + "\n\n")

    f.write(
        "Research Question:\n"
    )

    f.write(
        "What types of Technical Debt in test code are most frequently discussed "
        "and how are they addressed in Pull Requests?\n\n"
    )

    for title, table in [

        ("Test TD Mentioned", summary_mentioned),

        ("Mention Type", summary_mention_type),

        ("Test TD Type", summary_td_type)

    ]:

        f.write(title + "\n")

        f.write("-" * 50 + "\n")

        for _, row in table.iterrows():

            f.write(
                f"{row.iloc[0]}: "
                f"{row['Count']} "
                f"({row['Percentage']:.2f}%)\n"
            )

        f.write("\n")

    f.write("=" * 70 + "\n")

    f.write("Agreement by Test TD Type\n")

    f.write("=" * 70 + "\n\n")

    f.write(
        agreement_percentage.to_string()
    )

    f.write("\n\n")

    f.write("=" * 70 + "\n")

    f.write("Resolution by Test TD Type\n")

    f.write("=" * 70 + "\n\n")

    f.write(
        resolution_percentage.to_string()
    )

    f.write("\n")


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print()

print("=" * 70)

print("RQ4")

print("=" * 70)

print()

for title, table in [

    ("Test TD Mentioned", summary_mentioned),

    ("Mention Type", summary_mention_type),

    ("Test TD Type", summary_td_type)

]:

    print(title)

    print("-" * 40)

    print(table)

    print()

print("=" * 70)

print("How are Test TDs addressed?")

print("=" * 70)

print()

print("Agreement by Test TD Type")

print()

print(agreement_percentage)

print()

print("-" * 70)

print()

print("Resolution by Test TD Type")

print()

print(resolution_percentage)

print()

print("=" * 70)

print("GENERATED FILES")

print("=" * 70)

print()

print("test_td_mentioned.csv")
print("test_td_mentioned.xlsx")
print("test_td_mentioned_bar.png")
print("test_td_mentioned_pie.png")

print()

print("mention_type.csv")
print("mention_type.xlsx")
print("mention_type_bar.png")
print("mention_type_pie.png")

print()

print("test_td_type.csv")
print("test_td_type.xlsx")
print("test_td_type_bar.png")
print("test_td_type_pie.png")

print()

print("agreement_by_td_type.xlsx")
print("agreement_by_td_type_percentage.xlsx")

print()

print("resolution_by_td_type.xlsx")
print("resolution_by_td_type_percentage.xlsx")

print()

print("rq4_by_project.xlsx")
print("rq4_results.txt")

print()

print(f"Directory: {OUTPUT_DIR}")

print()

print("=" * 70)
