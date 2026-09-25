import json
import pandas as pd

from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill,
    Font,
    Alignment,
    Border,
    Side
)
from openpyxl.utils import get_column_letter

# =====================================================
# ARQUIVOS
# =====================================================

MANUAL_FILE = "data/manual_validation.xlsx"

LLM_FILE = "data/llm_results_validation.json"

OUTPUT_FILE = "results/validação/manual_validation_with_llm.xlsx"

# =====================================================
# CARREGA DADOS
# =====================================================

print("Lendo planilha manual...")

manual = pd.read_excel(MANUAL_FILE)

# Remove espaços antes/depois do nome das colunas
manual.columns = manual.columns.str.strip()

# Remove colunas totalmente vazias
manual = manual.loc[:, manual.columns != ""]

# Remove linhas vazias
manual = manual.dropna(subset=["repo", "pr_number"])

# Remove cabeçalhos repetidos
manual = manual[
    manual["repo"].astype(str).str.lower() != "repo"
]

manual = manual[
    manual["pr_number"].astype(str).str.lower() != "pr_number"
]

# Remove espaços
manual["pr_number"] = (
    manual["pr_number"]
    .astype(str)
    .str.strip()
    .str.replace("#", "", regex=False)
)

manual["pr_number"] = pd.to_numeric(
    manual["pr_number"],
    errors="coerce"
)

manual = manual.dropna(subset=["repo", "pr_number"])

manual["pr_number"] = manual["pr_number"].astype(int)

# Remove linhas vazias
manual = manual.dropna(subset=["repo", "pr_number"])

print("Lendo resultados da LLM...")

with open(
    LLM_FILE,
    encoding="utf8"
) as f:

    llm = json.load(f)

# =====================================================
# INDEXAÇÃO DOS RESULTADOS DA LLM
# =====================================================

llm_dict = {}

for pr in llm:

    chave = (

        pr["repo"],

        int(pr["pr_number"])

    )

    llm_dict[chave] = {

        "objetivo_pr":
            pr["primary_pr_objective"]["value"],

        "tipo_sugestao":
            pr["suggestion_type"]["value"],

        "acordo":
            pr["agreement"]["value"],

        "resolucao":
            pr["resolution"]["value"],

        "dt_teste_mencionada":
            pr["test_td_mentioned"]["value"],

        "forma_dt_menc":
            pr["mention_type"]["value"],

        "tipo_dt_teste":
            pr["test_td_type"]["value"]

    }

print(f"Resultados indexados: {len(llm_dict)}")

# =====================================================
# CRIA O EXCEL
# =====================================================

wb = Workbook()

ws = wb.active

ws.title = "Validation"

# =====================================================
# ESTILOS
# =====================================================

BLUE = PatternFill(
    "solid",
    fgColor="D9EAF7"
)

GREEN = PatternFill(
    "solid",
    fgColor="D9EAD3"
)

YELLOW = PatternFill(
    "solid",
    fgColor="FFF2CC"
)

ORANGE = PatternFill(
    "solid",
    fgColor="F9CB9C"
)

BORDER = Border(

    left=Side(style="thin"),

    right=Side(style="thin"),

    top=Side(style="thin"),

    bottom=Side(style="thin")

)

BOLD = Font(

    bold=True

)

CENTER = Alignment(

    horizontal="center",

    vertical="center"

)

# =====================================================
# CABEÇALHO PRINCIPAL
# =====================================================

grupos = [

    ("A1:B1",
     "Identification",
     BLUE),

    ("C1:E1",
     "RQ1 - Primary PR Objective",
     GREEN),

    ("F1:H1",
     "RQ2 - Suggestion Type",
     YELLOW),

    ("I1:K1",
     "RQ2 - Agreement",
     YELLOW),

    ("L1:N1",
     "RQ2 - Resolution",
     YELLOW),

    ("O1:Q1",
     "RQ4 - Test TD Mention",
     ORANGE),

    ("R1:T1",
     "RQ4 - Mention Type",
     ORANGE),

    ("U1:W1",
     "RQ4 - Test TD Type",
     ORANGE)

]

for intervalo, texto, cor in grupos:

    ws.merge_cells(intervalo)

    celula = ws[
        intervalo.split(":")[0]
    ]

    celula.value = texto

    celula.fill = cor

    celula.font = BOLD

    celula.alignment = CENTER

    celula.border = BORDER
    
# =====================================================
# SEGUNDA LINHA DO CABEÇALHO
# =====================================================

cabecalho = [

    "Repository",
    "PR",

    "Manual",
    "LLM",
    "Match",

    "Manual",
    "LLM",
    "Match",

    "Manual",
    "LLM",
    "Match",

    "Manual",
    "LLM",
    "Match",

    "Manual",
    "LLM",
    "Match",

    "Manual",
    "LLM",
    "Match",

    "Manual",
    "LLM",
    "Match"

]

cores = [

    BLUE,
    BLUE,

    GREEN,
    GREEN,
    GREEN,

    YELLOW,
    YELLOW,
    YELLOW,

    YELLOW,
    YELLOW,
    YELLOW,

    YELLOW,
    YELLOW,
    YELLOW,

    ORANGE,
    ORANGE,
    ORANGE,

    ORANGE,
    ORANGE,
    ORANGE,

    ORANGE,
    ORANGE,
    ORANGE

]

for coluna, texto in enumerate(cabecalho, start=1):

    cell = ws.cell(row=2, column=coluna)

    cell.value = texto

    cell.font = BOLD

    cell.alignment = CENTER

    cell.fill = cores[coluna - 1]

    cell.border = BORDER

# =====================================================
# DADOS
# =====================================================

linha = 3

for _, row in manual.iterrows():

    repo = row["repo"]
    pr_number = row["pr_number"]

    chave = (
        repo,
        pr_number
    )

    llm_data = llm_dict.get(chave, {})

    valores = [

        repo,
        pr_number,

        row["objetivo_pr"],
        llm_data.get("objetivo_pr", ""),
        "",

        row["tipo_sugestao"],
        llm_data.get("tipo_sugestao", ""),
        "",

        row["acordo"],
        llm_data.get("acordo", ""),
        "",

        row["resolucao"],
        llm_data.get("resolucao", ""),
        "",

        row["dt_teste_mencionada"],
        llm_data.get("dt_teste_mencionada", ""),
        "",

        row["forma_dt_menc"],
        llm_data.get("forma_dt_menc", ""),
        "",

        row["tipo_dt_teste"],
        llm_data.get("tipo_dt_teste", ""),
        ""

    ]

    for coluna, valor in enumerate(valores, start=1):

        cell = ws.cell(
            row=linha,
            column=coluna
        )

        cell.value = valor

        cell.alignment = CENTER

        cell.border = BORDER

    linha += 1

# =====================================================
# AJUSTE AUTOMÁTICO DAS COLUNAS
# =====================================================

for coluna in ws.columns:

    letra = get_column_letter(
        coluna[0].column
    )

    tamanho = 0

    for cell in coluna:

        if cell.value is not None:

            tamanho = max(
                tamanho,
                len(str(cell.value))
            )

    ws.column_dimensions[letra].width = min(
        tamanho + 3,
        35
    )

# Colunas Match menores

for coluna in [

    "E",
    "H",
    "K",
    "N",
    "Q",
    "T",
    "W"

]:

    ws.column_dimensions[coluna].width = 10

# =====================================================
# EXCEL
# =====================================================

ws.freeze_panes = "A3"

ws.auto_filter.ref = f"A2:W{ws.max_row}"

# =====================================================
# SALVA
# =====================================================

wb.save(OUTPUT_FILE)

print()

print("=" * 60)

print("PLANILHA GERADA COM SUCESSO")

print("=" * 60)

print()

print(f"Arquivo salvo em: {OUTPUT_FILE}")