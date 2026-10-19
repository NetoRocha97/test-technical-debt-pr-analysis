
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# FILE PATHS
# ==========================================================

RESULT_FILE = "data/llm_results_final.json"

OUTPUT_DIR = Path("results/rq2")

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
# CONVERT TO DATAFRAME
# ==========================================================

data = []

for pr in prs:

    data.append({

        "repo": pr["repo"],

        "suggestion_type": pr["suggestion_type"]["value"],

        "agreement": pr["agreement"]["value"],

        "resolution": pr["resolution"]["value"]

    })

df = pd.DataFrame(data)


# ==========================================================
# GENERATE STATISTICS
# ==========================================================

def generate_statistics(
    dataframe,
    column,
    output_name
):

    summary = (

        dataframe[column]

        .value_counts()

        .rename_axis(column)

        .reset_index(name="Count")

    )

    summary["Percentage"] = (

        summary["Count"]

        / summary["Count"].sum()

        * 100

    ).round(2)

    csv_file = OUTPUT_DIR / f"{output_name}.csv"

    xlsx_file = OUTPUT_DIR / f"{output_name}.xlsx"

    bar_file = OUTPUT_DIR / f"{output_name}_bar.png"

    pie_file = OUTPUT_DIR / f"{output_name}_pie.png"

    summary.to_csv(
        csv_file,
        index=False,
        encoding="utf8"
    )

    summary.to_excel(
        xlsx_file,
        index=False
    )

    return (
        summary,
        csv_file,
        xlsx_file,
        bar_file,
        pie_file
    )


# ==========================================================
# GENERATE CHARTS
# ==========================================================

def generate_charts(
    summary,
    title,
    bar_file,
    pie_file
):

    plt.figure(
        figsize=(9, 5)
    )

    bars = plt.bar(
        summary.iloc[:, 0],
        summary["Count"]
    )

    plt.title(title)

    plt.xlabel("Category")

    plt.ylabel("Number of PRs")

    plt.xticks(rotation=20)

    for bar in bars:

        height = bar.get_height()

        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()

    plt.savefig(
        bar_file,
        dpi=300
    )

    plt.close()

    plt.figure(
        figsize=(7, 7)
    )

    plt.pie(
        summary["Count"],
        labels=summary.iloc[:, 0],
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(title)

    plt.tight_layout()

    plt.savefig(
        pie_file,
        dpi=300
    )

    plt.close()


# ==========================================================
# GENERATE PER-PROJECT STATISTICS
# ==========================================================

with pd.ExcelWriter(
    OUTPUT_DIR / "rq2_by_project.xlsx",
    engine="openpyxl"
) as project_writer:

    for column in [
        "suggestion_type",
        "agreement",
        "resolution"
    ]:

        table = pd.crosstab(
            df["repo"],
            df[column]
        )

        table.to_excel(
            project_writer,
            sheet_name=column[:31]
        )


# ==========================================================
# RUN STATISTICAL ANALYSIS
# ==========================================================

suggestion_result = generate_statistics(
    df,
    "suggestion_type",
    "suggestion_type"
)

agreement_result = generate_statistics(
    df,
    "agreement",
    "agreement"
)

resolution_result = generate_statistics(
    df,
    "resolution",
    "resolution"
)


# ==========================================================
# GENERATE CHARTS
# ==========================================================

for result, title in [

    (suggestion_result, "RQ2 - Suggestion Type"),

    (agreement_result, "RQ2 - Agreement"),

    (resolution_result, "RQ2 - Resolution")

]:

    generate_charts(
        result[0],
        title,
        result[3],
        result[4]
    )


# ==========================================================
# GENERATE TEXT SUMMARY
# ==========================================================

TXT_FILE = OUTPUT_DIR / "rq2_results.txt"

with open(
    TXT_FILE,
    "w",
    encoding="utf8"
) as f:

    f.write("=" * 60 + "\n")
    f.write("RQ2\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        "Research Question:\n"
    )

    f.write(
        "What are the key characteristics of suggestions for addressing Technical Debt issues?\n\n"
    )

    for name, result in [

        ("Suggestion Type", suggestion_result),

        ("Agreement", agreement_result),

        ("Resolution", resolution_result)

    ]:

        table = result[0]

        f.write(f"{name}\n")
        f.write("-" * 40 + "\n")

        for _, row in table.iterrows():

            f.write(
                f"{row.iloc[0]}: "
                f"{row['Count']} "
                f"({row['Percentage']:.2f}%)\n"
            )

        f.write("\n")


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print()

print("=" * 70)

print("RQ2")

print("=" * 70)

for name, result in [

    ("Suggestion Type", suggestion_result),

    ("Agreement", agreement_result),

    ("Resolution", resolution_result)

]:

    print()

    print(name)

    print("-" * 40)

    print(result[0])

print()

print("=" * 70)

print("GENERATED FILES")

print("=" * 70)

for name in [
    "suggestion_type",
    "agreement",
    "resolution"
]:

    print()

    print(f"{name}.csv")

    print(f"{name}.xlsx")

    print(f"{name}_bar.png")

    print(f"{name}_pie.png")

print()

print("rq2_results.txt")

print("rq2_by_project.xlsx")

print()

print(f"Directory: {OUTPUT_DIR}")

print()

print("=" * 70)
