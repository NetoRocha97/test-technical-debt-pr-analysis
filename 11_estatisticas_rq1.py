import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# ARQUIVOS
# ==========================================================

RESULT_FILE = "data/llm_results_final.json"

OUTPUT_DIR = Path("results/rq1")

CSV_FILE = OUTPUT_DIR / "rq1_summary.csv"

XLSX_FILE = OUTPUT_DIR / "rq1_summary.xlsx"

BAR_FILE = OUTPUT_DIR / "rq1_bar.png"

PIE_FILE = OUTPUT_DIR / "rq1_pie.png"

TXT_FILE = OUTPUT_DIR / "rq1_results.txt"

PROJECT_FILE = OUTPUT_DIR / "rq1_by_project.xlsx"


# ==========================================================
# CARREGA JSON
# ==========================================================

def carregar_resultados():

    with open(
        RESULT_FILE,
        encoding="utf8"
    ) as f:

        return json.load(f)


# ==========================================================
# CRIA PASTA
# ==========================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# DADOS
# ==========================================================

prs = carregar_resultados()

dados = []

for pr in prs:

    dados.append({

        "repo":

            pr["repo"],

        "objective":

            pr["primary_pr_objective"]["value"]

    })

df = pd.DataFrame(dados)


# ==========================================================
# ESTATÍSTICAS
# ==========================================================

summary = (

    df["objective"]

    .value_counts()

    .rename_axis("Objective")

    .reset_index(name="Count")

)

summary["Percentage"] = (

    summary["Count"]

    / summary["Count"].sum()

    * 100

).round(2)


# ==========================================================
# EXPORTA CSV
# ==========================================================

summary.to_csv(

    CSV_FILE,

    index=False,

    encoding="utf8"

)


# ==========================================================
# EXPORTA EXCEL
# ==========================================================

summary.to_excel(

    XLSX_FILE,

    index=False

)


# ==========================================================
# POR PROJETO
# ==========================================================

project_summary = pd.crosstab(

    df["repo"],

    df["objective"]

)

project_summary.to_excel(

    PROJECT_FILE

)


# ==========================================================
# GRÁFICO DE BARRAS
# ==========================================================

plt.figure(

    figsize=(8,5)

)

plt.bar(

    summary["Objective"],

    summary["Count"]

)

plt.title(

    "RQ1 - Primary PR Objective"

)

plt.xlabel(

    "Objective"

)

plt.ylabel(

    "Number of PRs"

)

plt.tight_layout()

plt.savefig(

    BAR_FILE,

    dpi=300

)

plt.close()

# ==========================================================
# GRÁFICO DE PIZZA
# ==========================================================

plt.figure(figsize=(7, 7))

plt.pie(
    summary["Count"],
    labels=summary["Objective"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("RQ1 - Primary PR Objective")

plt.tight_layout()

plt.savefig(
    PIE_FILE,
    dpi=300
)

plt.close()


# ==========================================================
# RESUMO TXT
# ==========================================================

total = summary["Count"].sum()

mais_frequente = summary.iloc[0]

with open(
    TXT_FILE,
    "w",
    encoding="utf8"
) as f:

    f.write("=" * 60 + "\n")
    f.write("RQ1\n")
    f.write("=" * 60 + "\n\n")

    f.write(
        "Research Question:\n"
    )

    f.write(
        "Which maintenance goals are commonly linked to PRs that discuss Technical Debt?\n\n"
    )

    f.write(
        f"Total PRs analysed: {total}\n\n"
    )

    f.write(
        "Frequency of maintenance goals:\n\n"
    )

    for _, row in summary.iterrows():

        f.write(
            f"{row['Objective']}: "
            f"{row['Count']} "
            f"({row['Percentage']:.2f}%)\n"
        )

    f.write("\n")

    f.write(
        "Most frequent maintenance goal:\n"
    )

    f.write(
        f"{mais_frequente['Objective']} "
        f"({mais_frequente['Count']} PRs - "
        f"{mais_frequente['Percentage']:.2f}%)\n"
    )


# ==========================================================
# TERMINAL
# ==========================================================

print()

print("=" * 60)

print("RQ1")

print("=" * 60)

print()

print(summary)

print()

print(f"Total PRs: {total}")

print()

print("Arquivos gerados:")

print(f"CSV   : {CSV_FILE}")

print(f"Excel : {XLSX_FILE}")

print(f"Bar   : {BAR_FILE}")

print(f"Pie   : {PIE_FILE}")

print(f"TXT   : {TXT_FILE}")

print(f"Repo  : {PROJECT_FILE}")

print()

print("=" * 60)