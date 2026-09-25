import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# ARQUIVOS
# ==========================================================

RESULT_FILE = "data/llm_results_final.json"

OUTPUT_DIR = Path("results/rq2")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# CARREGA RESULTADOS
# ==========================================================

with open(
    RESULT_FILE,
    encoding="utf8"
) as f:

    prs = json.load(f)


# ==========================================================
# CONVERTE PARA DATAFRAME
# ==========================================================

dados = []

for pr in prs:

    dados.append({

        "repo":

            pr["repo"],

        "suggestion_type":

            pr["suggestion_type"]["value"],

        "agreement":

            pr["agreement"]["value"],

        "resolution":

            pr["resolution"]["value"]

    })

df = pd.DataFrame(dados)


# ==========================================================
# FUNÇÃO PARA GERAR ESTATÍSTICAS
# ==========================================================

def gerar_estatisticas(
    dataframe,
    coluna,
    nome_saida
):

    summary = (

        dataframe[coluna]

        .value_counts()

        .rename_axis(coluna)

        .reset_index(name="Count")

    )

    summary["Percentage"] = (

        summary["Count"]

        / summary["Count"].sum()

        * 100

    ).round(2)

    csv_file = OUTPUT_DIR / f"{nome_saida}.csv"

    xlsx_file = OUTPUT_DIR / f"{nome_saida}.xlsx"

    bar_file = OUTPUT_DIR / f"{nome_saida}_bar.png"

    pie_file = OUTPUT_DIR / f"{nome_saida}_pie.png"

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
# GRÁFICOS
# ==========================================================

def gerar_graficos(

    summary,

    titulo,

    bar_file,

    pie_file

):

    # -------------------------
    # BARRAS
    # -------------------------

    plt.figure(

        figsize=(9, 5)

    )

    bars = plt.bar(

        summary.iloc[:, 0],

        summary["Count"]

    )

    plt.title(titulo)

    plt.xlabel("Category")

    plt.ylabel("Number of PRs")

    plt.xticks(rotation=20)

    for bar in bars:

        altura = bar.get_height()

        plt.text(

            bar.get_x() + bar.get_width()/2,

            altura,

            f"{int(altura)}",

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

    # -------------------------
    # PIZZA
    # -------------------------

    plt.figure(

        figsize=(7, 7)

    )

    plt.pie(

        summary["Count"],

        labels=summary.iloc[:, 0],

        autopct="%1.1f%%",

        startangle=90

    )

    plt.title(titulo)

    plt.tight_layout()

    plt.savefig(

        pie_file,

        dpi=300

    )

    plt.close()


# ==========================================================
# ESTATÍSTICAS POR PROJETO
# ==========================================================

project_writer = pd.ExcelWriter(

    OUTPUT_DIR / "rq2_by_project.xlsx",

    engine="openpyxl"

)

for coluna in [

    "suggestion_type",

    "agreement",

    "resolution"

]:

    tabela = pd.crosstab(

        df["repo"],

        df[coluna]

    )

    tabela.to_excel(

        project_writer,

        sheet_name=coluna[:31]

    )

project_writer.close()


# ==========================================================
# EXECUTA
# ==========================================================

resultado_suggestion = gerar_estatisticas(

    df,

    "suggestion_type",

    "suggestion_type"

)

resultado_agreement = gerar_estatisticas(

    df,

    "agreement",

    "agreement"

)

resultado_resolution = gerar_estatisticas(

    df,

    "resolution",

    "resolution"

)

# ==========================================================
# GERA GRÁFICOS
# ==========================================================

for resultado, titulo in [

    (resultado_suggestion, "RQ2 - Suggestion Type"),

    (resultado_agreement, "RQ2 - Agreement"),

    (resultado_resolution, "RQ2 - Resolution")

]:

    gerar_graficos(

        resultado[0],

        titulo,

        resultado[3],

        resultado[4]

    )


# ==========================================================
# GERA RESUMO TXT
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

    for nome, resultado in [

        ("Suggestion Type", resultado_suggestion),

        ("Agreement", resultado_agreement),

        ("Resolution", resultado_resolution)

    ]:

        tabela = resultado[0]

        f.write(f"{nome}\n")
        f.write("-" * 40 + "\n")

        for _, row in tabela.iterrows():

            f.write(

                f"{row.iloc[0]}: "

                f"{row['Count']} "

                f"({row['Percentage']:.2f}%)\n"

            )

        f.write("\n")


# ==========================================================
# TERMINAL
# ==========================================================

print()

print("=" * 70)

print("RQ2")

print("=" * 70)

for nome, resultado in [

    ("Suggestion Type", resultado_suggestion),

    ("Agreement", resultado_agreement),

    ("Resolution", resultado_resolution)

]:

    print()

    print(nome)

    print("-" * 40)

    print(resultado[0])

print()

print("=" * 70)

print("Arquivos gerados")

print("=" * 70)

for nome in [

    "suggestion_type",

    "agreement",

    "resolution"

]:

    print()

    print(f"{nome}.csv")

    print(f"{nome}.xlsx")

    print(f"{nome}_bar.png")

    print(f"{nome}_pie.png")

print()

print("rq2_results.txt")

print("rq2_by_project.xlsx")

print()

print(f"Pasta: {OUTPUT_DIR}")

print()

print("=" * 70)