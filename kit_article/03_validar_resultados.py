import json

from schema import ANALYSIS_SCHEMA

RESULT_FILE = "data/llm_results.json"


def validar_enum(valor, permitidos, campo):

    if valor not in permitidos:
        raise ValueError(
            f"{campo}: valor inválido -> {valor}"
        )


def validar_thread(thread):

    validar_enum(
        thread["scope"],
        [
            "TEST",
            "PRODUCTION",
            "MIXED",
            "UNKNOWN"
        ],
        "scope"
    )

    validar_enum(
        thread["test_td_discussion"],
        [
            "YES",
            "NO",
            "UNCERTAIN"
        ],
        "test_td_discussion"
    )

    validar_enum(
        thread["test_td_category"],
        [
            "Assertion",
            "Exception Handling",
            "Test Failure",
            "Test Fragility",
            "Test Maintainability",
            "Test Readability",
            "Test Design",
            "Test Execution",
            "Test Smell",
            "Test Fixture",
            "Test Dependency",
            "Test Data",
            "Test Duplication",
            "Test Refactoring",
            "Other",
            "UNKNOWN"
        ],
        "test_td_category"
    )

    validar_enum(
        thread["contains_suggestion"],
        [
            "YES",
            "NO"
        ],
        "contains_suggestion"
    )

    validar_enum(
        thread["suggestion_type"],
        [
            "EXPLICIT",
            "IMPLICIT",
            "NONE",
            "UNKNOWN"
        ],
        "suggestion_type"
    )

    validar_enum(
        thread["agreement"],
        [
            "AGREED",
            "REJECTED",
            "POSTPONED",
            "IGNORED",
            "UNKNOWN"
        ],
        "agreement"
    )

    validar_enum(
        thread["resolution"],
        [
            "FIXED",
            "P-FIXED",
            "UNFIXED",
            "UNKNOWN"
        ],
        "resolution"
    )

    if not (0 <= thread["confidence"] <= 1):
        raise ValueError(
            f"confidence inválido: {thread['confidence']}"
        )


def validar_pr(pr):

    campos = ANALYSIS_SCHEMA["required"]

    for campo in campos:

        if campo not in pr:

            raise ValueError(
                f"Campo ausente: {campo}"
            )

    for thread in pr["threads"]:

        validar_thread(thread)


def main():

    with open(
        RESULT_FILE,
        encoding="utf8"
    ) as f:

        resultados = json.load(f)

    print()

    print(f"PRs analisados: {len(resultados)}")

    erros = 0

    for pr in resultados:

        try:

            validar_pr(pr)

        except Exception as e:

            erros += 1

            print()

            print(
                f"{pr['repo']} #{pr['pr_number']}"
            )

            print(e)

    print()

    if erros == 0:

        print("Todos os resultados são válidos.")

    else:

        print(f"Foram encontrados {erros} erro(s).")


if __name__ == "__main__":

    main()