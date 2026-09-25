import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ==========================================================
# ARQUIVOS
# ==========================================================

RESULT_FILE = "data/llm_results_final.json"

OUTPUT_DIR = Path("results/rq4")

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
# DATAFRAME
# ==========================================================

dados = []

for pr in prs:

    dados.append({

        "repo":
            pr["repo"],

        "test_td_mentioned":
            pr["test_td_mentioned"]["value"],

        "mention_type":
            pr["mention_type"]["value"],

        "test_td_type":
            pr["test_td_type"]["value"],

        "agreement":
            pr["agreement"]["value"],

        "resolution":
            pr["resolution"]["value"]

    })

df = pd.DataFrame(dados)

# ==========================================================
# FUNÇÕES
# ==========================================================

def gerar_resumo(coluna):

    resumo = (

        df[coluna]

        .value_counts()

        .rename_axis(coluna)

        .reset_index(name="Count")

    )

    resumo["Percentage"] = (

        resumo["Count"]

        / resumo["Count"].sum()

        * 100

    ).round(2)

    return resumo


def salvar_tabela(resumo, nome):

    csv_file = OUTPUT_DIR / f"{nome}.csv"

    xlsx_file = OUTPUT_DIR / f"{nome}.xlsx"

    resumo.to_csv(

        csv_file,

        index=False,

        encoding="utf8"

    )

    resumo.to_excel(

        xlsx_file,

        index=False

    )

    return csv_file, xlsx_file

# ==========================================================
# GRÁFICOS
# ==========================================================

def gerar_graficos(resumo, titulo, nome):

    # -------------------------
    # Barras
    # -------------------------

    plt.figure(figsize=(9,5))

    bars = plt.bar(

        resumo.iloc[:,0],

        resumo["Count"]

    )

    plt.title(titulo)

    plt.xlabel("Category")

    plt.ylabel("Number of PRs")

    plt.xticks(rotation=25)

    for bar in bars:

        altura = bar.get_height()

        plt.text(

            bar.get_x() + bar.get_width()/2,

            altura,

            str(int(altura)),

            ha="center",

            va="bottom",

            fontsize=9

        )

    plt.tight_layout()

    plt.savefig(

        OUTPUT_DIR / f"{nome}_bar.png",

        dpi=300

    )

    plt.close()

    # -------------------------
    # Pizza
    # -------------------------

    plt.figure(figsize=(7,7))

    plt.pie(

        resumo["Count"],

        labels=resumo.iloc[:,0],

        autopct="%1.1f%%",

        startangle=90

    )

    plt.title(titulo)

    plt.tight_layout()

    plt.savefig(

        OUTPUT_DIR / f"{nome}_pie.png",

        dpi=300

    )

    plt.close()


# ==========================================================
# ESTATÍSTICAS PRINCIPAIS
# ==========================================================

summary_mentioned = gerar_resumo(

    "test_td_mentioned"

)

summary_mention_type = gerar_resumo(

    "mention_type"

)

summary_td_type = gerar_resumo(

    "test_td_type"

)


salvar_tabela(

    summary_mentioned,

    "test_td_mentioned"

)

salvar_tabela(

    summary_mention_type,

    "mention_type"

)

salvar_tabela(

    summary_td_type,

    "test_td_type"

)


gerar_graficos(

    summary_mentioned,

    "RQ4 - Test TD Mentioned",

    "test_td_mentioned"

)

gerar_graficos(

    summary_mention_type,

    "RQ4 - Mention Type",

    "mention_type"

)

gerar_graficos(

    summary_td_type,

    "RQ4 - Test TD Type",

    "test_td_type"

)

# ==========================================================
# HOW ARE THEY ADDRESSED?
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
# PORCENTAGENS POR LINHA
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
# ESTATÍSTICAS POR PROJETO
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
# RELATÓRIO TXT
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

    for titulo, tabela in [

        ("Test TD Mentioned", summary_mentioned),

        ("Mention Type", summary_mention_type),

        ("Test TD Type", summary_td_type)

    ]:

        f.write(titulo + "\n")

        f.write("-" * 50 + "\n")

        for _, row in tabela.iterrows():

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
# TERMINAL
# ==========================================================

print()

print("=" * 70)

print("RQ4")

print("=" * 70)

print()

for titulo, tabela in [

    ("Test TD Mentioned", summary_mentioned),

    ("Mention Type", summary_mention_type),

    ("Test TD Type", summary_td_type)

]:

    print(titulo)

    print("-" * 40)

    print(tabela)

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

print("Arquivos gerados")

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

print(f"Pasta: {OUTPUT_DIR}")

print()

print("=" * 70)