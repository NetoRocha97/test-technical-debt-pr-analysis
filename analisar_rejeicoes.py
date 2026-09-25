import json
import time
from pathlib import Path
import os

from openai import OpenAI

from prompt_rejection import build_messages
from schema_rejection import RESPONSE_FORMAT

# =====================================================
# CONFIGURAÇÃO
# =====================================================

API_KEY = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-5.5"

client = OpenAI(api_key=API_KEY)

DATASET_FILE = "data/prs_rejected.json"

RESULT_FILE = "data/rejection_reasons.json"

# =====================================================
# LEITURA DOS ARQUIVOS
# =====================================================

def carregar_dataset():

    with open(
        DATASET_FILE,
        encoding="utf8"
    ) as f:

        return json.load(f)


# =====================================================
# RESULTADOS
# =====================================================

def carregar_resultados():

    if Path(RESULT_FILE).exists():

        with open(
            RESULT_FILE,
            encoding="utf8"
        ) as f:

            return json.load(f)

    return []


def salvar_resultados(resultados):

    with open(
        RESULT_FILE,
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            resultados,
            f,
            indent=2,
            ensure_ascii=False
        )


# =====================================================
# CONVERTE COMENTÁRIOS
# =====================================================

def formatar_review_threads(pr):

    linhas = []

    if len(pr["review_threads"]) == 0:

        return "None"

    for thread in pr["review_threads"]:

        linhas.append("-" * 60)

        linhas.append(

            f"Thread: {thread['thread_id']} | "

            f"File: {thread['path']} | "

            f"Line: {thread['line']}"

        )

        for comment in thread["comments"]:

            linhas.append(

                f"{comment['author']} ({comment['created_at']}):"

            )

            linhas.append(

                comment["body"]

            )

            linhas.append("")

    return "\n".join(linhas)

# =====================================================
# ANÁLISE COM A LLM
# =====================================================

def analisar_pr(pr):

    comentarios = formatar_review_threads(pr)

    if pr["issue_comments"]:

        comentarios += "\n\n# Issue Comments\n\n"

        for c in pr["issue_comments"]:

            comentarios += (

                f"{c['author']} ({c['created_at']}):\n"

            )

            comentarios += c["body"]

            comentarios += "\n\n"

    pr_llm = {

        "repo": pr["repo"],

        "pr_number": pr["pr_number"],

        "title": pr["title"],

        "description": pr["description"],

        "comments": comentarios

    }

    mensagens = build_messages(pr_llm)

    for tentativa in range(3):

        try:

            response = client.responses.create(

                model=MODEL,

                input=mensagens,

                text={

                    "format": RESPONSE_FORMAT

                }

            )

            return json.loads(

                response.output_text

            )

        except Exception as e:

            print(

                f"Tentativa {tentativa + 1}/3 falhou."

            )

            print(e)

            time.sleep(3)

    return None

# =====================================================
# MAIN
# =====================================================

def main():

    dataset = carregar_dataset()

    resultados = carregar_resultados()

    prs_processados = {

        (r["repo"], r["pr_number"])

        for r in resultados

    }

    total = len(dataset)

    print(f"Dataset: {total} PR(s)")

    print(f"Resultados existentes: {len(resultados)}")

    for i, pr in enumerate(dataset, start=1):

        chave = (

            pr["repo"],

            pr["pr_number"]

        )

        if chave in prs_processados:

            continue

        print(

            f"\n[{i}/{total}] "

            f"{pr['repo']} "

            f"#{pr['pr_number']}"

        )

        resultado = analisar_pr(pr)

        if resultado is None:

            print("Falhou.")

            continue

        resultados.append(resultado)

        salvar_resultados(resultados)

        print(

            f"Motivo: "

            f"{resultado['rejection_reason']['value']}"

        )

        print("OK")

        time.sleep(1)

    print()

    print("=" * 60)

    print("PROCESSAMENTO FINALIZADO")

    print("=" * 60)

    print()

    print(f"Resultados salvos em:")

    print(RESULT_FILE)

    print()

    print("=" * 60)


if __name__ == "__main__":

    main()