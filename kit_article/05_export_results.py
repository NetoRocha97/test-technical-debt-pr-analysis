import json
import csv
from pathlib import Path

RESULT_FILE = "data/llm_results.json"
OUTPUT_DIR = Path("results")


def garantir_pasta():
    OUTPUT_DIR.mkdir(exist_ok=True)


def carregar_resultados():
    with open(RESULT_FILE, encoding="utf8") as f:
        return json.load(f)


def salvar_csv(nome, cabecalho, linhas):

    caminho = OUTPUT_DIR / nome

    with open(
        caminho,
        "w",
        newline="",
        encoding="utf8"
    ) as f:

        writer = csv.writer(f)
        writer.writerow(cabecalho)
        writer.writerows(linhas)


# =====================================================
# RQ1
# =====================================================

def exportar_rq1(prs):

    linhas = []

    for pr in prs:

        linhas.append([

            pr["repo"],
            pr["pr_number"],
            pr["primary_pr_objective"],
            pr["contains_test_td_discussion"]

        ])

    salvar_csv(

        "RQ1_Objectives.csv",

        [

            "Repository",
            "PR",
            "PrimaryObjective",
            "ContainsTestTD"

        ],

        linhas

    )


# =====================================================
# RQ2
# =====================================================

def exportar_rq2(prs):

    linhas = []

    for pr in prs:

        for thread in pr["threads"]:

            linhas.append([

                pr["repo"],
                pr["pr_number"],

                thread["thread_id"],

                thread["scope"],

                thread["test_td_discussion"],

                thread["test_td_category"],

                thread["contains_suggestion"],

                thread["suggestion_type"],

                thread["suggestion_author"],

                thread["contains_code_suggestion"],

                thread["agreement"],

                thread["resolution"]

            ])

    salvar_csv(

        "RQ2_Suggestions.csv",

        [

            "Repository",

            "PR",

            "Thread",

            "Scope",

            "TestTDDiscussion",

            "TestTDCategory",

            "ContainsSuggestion",

            "SuggestionType",

            "SuggestionAuthor",

            "ContainsCodeSuggestion",

            "Agreement",

            "Resolution"

        ],

        linhas

    )
    
# =====================================================
# RQ3
# =====================================================

def exportar_rq3(prs):

    linhas = []

    for pr in prs:

        for thread in pr["threads"]:

            if thread["agreement"] != "REJECTED":
                continue

            linhas.append([

                pr["repo"],

                pr["pr_number"],

                thread["thread_id"],

                thread["test_td_category"],

                thread["suggestion_type"],

                thread["suggestion_author"],

                thread["rejection_reason"],

                thread["justification"]

            ])

    salvar_csv(

        "RQ3_RejectionReasons.csv",

        [

            "Repository",

            "PR",

            "Thread",

            "TestTDCategory",

            "SuggestionType",

            "SuggestionAuthor",

            "RejectionReason",

            "Justification"

        ],

        linhas

    )


# =====================================================
# RQ4
# =====================================================

def exportar_rq4(prs):

    convergencia = []

    divergencia = []

    novidade = []

    for pr in prs:

        for thread in pr["threads"]:

            regras = []

            for regra in thread["convergence"]["related_rules"]:

                regras.append(regra["rule"])

            convergencia.append([

                pr["repo"],

                pr["pr_number"],

                thread["thread_id"],

                thread["convergence"]["classification"],

                "; ".join(regras)

            ])

            divergencia.append([

                pr["repo"],

                pr["pr_number"],

                thread["thread_id"],

                thread["divergence"]["classification"],

                thread["divergence"]["explanation"]

            ])

            novidade.append([

                pr["repo"],

                pr["pr_number"],

                thread["thread_id"],

                thread["novelty"]["classification"],

                thread["novelty"]["explanation"]

            ])

    salvar_csv(

        "RQ4_Convergence.csv",

        [

            "Repository",

            "PR",

            "Thread",

            "Classification",

            "RelatedRules"

        ],

        convergencia

    )

    salvar_csv(

        "RQ4_Divergence.csv",

        [

            "Repository",

            "PR",

            "Thread",

            "Classification",

            "Explanation"

        ],

        divergencia

    )

    salvar_csv(

        "RQ4_Novelty.csv",

        [

            "Repository",

            "PR",

            "Thread",

            "Classification",

            "Explanation"

        ],

        novidade

    )
    
# =====================================================
# ALL THREADS
# =====================================================

def exportar_all_threads(prs):

    linhas = []

    for pr in prs:

        for thread in pr["threads"]:

            regras = []

            for regra in thread["convergence"]["related_rules"]:

                regras.append(regra["rule"])

            linhas.append([

                pr["repo"],

                pr["pr_number"],

                pr["primary_pr_objective"],

                pr["contains_test_td_discussion"],

                thread["thread_id"],

                thread["file"],

                thread["line"],

                thread["scope"],

                thread["test_td_discussion"],

                thread["test_td_category"],

                thread["contains_suggestion"],

                thread["suggestion_type"],

                thread["suggestion_author"],

                thread["contains_code_suggestion"],

                thread["agreement"],

                thread["resolution"],

                thread["rejection_reason"],

                thread["convergence"]["classification"],

                thread["divergence"]["classification"],

                thread["novelty"]["classification"],

                "; ".join(regras),

                thread["confidence"],

                thread["confidence_reason"]

            ])

    salvar_csv(

        "All_Threads.csv",

        [

            "Repository",

            "PR",

            "PrimaryObjective",

            "ContainsTestTD",

            "Thread",

            "File",

            "Line",

            "Scope",

            "TestTDDiscussion",

            "TestTDCategory",

            "ContainsSuggestion",

            "SuggestionType",

            "SuggestionAuthor",

            "ContainsCodeSuggestion",

            "Agreement",

            "Resolution",

            "RejectionReason",

            "Convergence",

            "Divergence",

            "Novelty",

            "RelatedRules",

            "Confidence",

            "ConfidenceReason"

        ],

        linhas

    )
    
# =====================================================
# SUMMARY
# =====================================================

def gerar_summary(prs):

    total_prs = len(prs)

    total_threads = sum(
        len(pr["threads"])
        for pr in prs
    )

    prs_com_td = sum(
        1
        for pr in prs
        if pr["contains_test_td_discussion"] == "YES"
    )

    with open(
        OUTPUT_DIR / "summary.txt",
        "w",
        encoding="utf8"
    ) as f:

        f.write("=====================================\n")
        f.write("LLM ANALYSIS SUMMARY\n")
        f.write("=====================================\n\n")

        f.write(f"Total PRs: {total_prs}\n")
        f.write(f"PRs containing Test Technical Debt discussions: {prs_com_td}\n")
        f.write(f"Total review threads analyzed: {total_threads}\n")


# =====================================================
# MAIN
# =====================================================

def main():

    garantir_pasta()

    prs = carregar_resultados()

    exportar_rq1(prs)

    exportar_rq2(prs)

    exportar_rq3(prs)

    exportar_rq4(prs)

    exportar_all_threads(prs)

    gerar_summary(prs)

    print()
    print("=" * 60)
    print("EXPORT COMPLETED")
    print("=" * 60)

    print(f"\nResults folder: {OUTPUT_DIR.resolve()}")

    print("\nGenerated files:")

    arquivos = sorted(OUTPUT_DIR.glob("*"))

    for arquivo in arquivos:

        print(f" - {arquivo.name}")

    print()


if __name__ == "__main__":

    main()