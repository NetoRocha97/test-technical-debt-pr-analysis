import json
from collections import Counter

RESULT_FILE = "data/llm_results.json"


def imprimir_counter(titulo, counter):

    print(f"\n{titulo}")
    print("-" * len(titulo))

    total = sum(counter.values())

    for chave, valor in counter.most_common():

        percentual = 0

        if total > 0:
            percentual = valor / total * 100

        print(f"{chave:25} {valor:5} ({percentual:5.1f}%)")


def main():

    with open(RESULT_FILE, encoding="utf8") as f:
        prs = json.load(f)

    objetivo_counter = Counter()

    scope_counter = Counter()

    td_counter = Counter()

    categoria_counter = Counter()

    sugestao_counter = Counter()

    tipo_sugestao_counter = Counter()

    autor_sugestao_counter = Counter()

    codigo_counter = Counter()

    acordo_counter = Counter()

    resolucao_counter = Counter()

    rejeicao_counter = Counter()

    convergencia_counter = Counter()

    divergencia_counter = Counter()

    novidade_counter = Counter()

    regras_counter = Counter()

    total_threads = 0

    prs_com_td = 0

    for pr in prs:

        objetivo_counter[pr["primary_pr_objective"]] += 1

        if pr["contains_test_td_discussion"] == "YES":
            prs_com_td += 1

        for thread in pr["threads"]:

            total_threads += 1

            scope_counter[thread["scope"]] += 1

            td_counter[thread["test_td_discussion"]] += 1

            categoria_counter[
                thread["test_td_category"]
            ] += 1

            sugestao_counter[
                thread["contains_suggestion"]
            ] += 1

            tipo_sugestao_counter[
                thread["suggestion_type"]
            ] += 1

            autor_sugestao_counter[
                thread["suggestion_author"]
            ] += 1

            codigo_counter[
                thread["contains_code_suggestion"]
            ] += 1

            acordo_counter[
                thread["agreement"]
            ] += 1

            resolucao_counter[
                thread["resolution"]
            ] += 1

            rejeicao_counter[
                thread["rejection_reason"]
            ] += 1

            convergencia_counter[
                thread["convergence"]["classification"]
            ] += 1

            divergencia_counter[
                thread["divergence"]["classification"]
            ] += 1

            novidade_counter[
                thread["novelty"]["classification"]
            ] += 1

            for regra in thread["convergence"]["related_rules"]:

                regras_counter[
                    regra["rule"]
                ] += 1

    print("\n===================================================")
    print("GENERAL")
    print("===================================================")

    print(f"PRs analisados              : {len(prs)}")
    print(f"PRs com Test TD             : {prs_com_td}")
    print(f"Threads analisadas          : {total_threads}")

    print("\n===================================================")
    print("RQ1")
    print("Maintenance objectives")
    print("===================================================")

    imprimir_counter(
        "Primary PR Objective",
        objetivo_counter
    )

    print("\n===================================================")
    print("RQ2")
    print("Characteristics of suggestions")
    print("===================================================")

    imprimir_counter(
        "Scope",
        scope_counter
    )

    imprimir_counter(
        "Test TD Discussion",
        td_counter
    )

    imprimir_counter(
        "Test TD Category",
        categoria_counter
    )

    imprimir_counter(
        "Contains Suggestion",
        sugestao_counter
    )

    imprimir_counter(
        "Suggestion Type",
        tipo_sugestao_counter
    )

    imprimir_counter(
        "Suggestion Author",
        autor_sugestao_counter
    )

    imprimir_counter(
        "Contains Code Suggestion",
        codigo_counter
    )

    imprimir_counter(
        "Agreement",
        acordo_counter
    )

    imprimir_counter(
        "Resolution",
        resolucao_counter
    )

    print("\n===================================================")
    print("RQ3")
    print("Reasons for rejection")
    print("===================================================")

    imprimir_counter(
        "Rejection Reason",
        rejeicao_counter
    )

    print("\n===================================================")
    print("RQ4")
    print("Comparison with SonarQube")
    print("===================================================")

    imprimir_counter(
        "Convergence",
        convergencia_counter
    )

    imprimir_counter(
        "Divergence",
        divergencia_counter
    )

    imprimir_counter(
        "Novelty",
        novidade_counter
    )

    imprimir_counter(
        "Related Sonar Rules",
        regras_counter
    )


if __name__ == "__main__":
    main()