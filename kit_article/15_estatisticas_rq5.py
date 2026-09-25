import json
import pandas as pd

LLM_FILE = "data/llm_results_final.json"
SONAR_FILE = "data/filtered_test_processed_issues.csv"

OUTPUT_FILE = "results/rq5_sonarqube_comparison.csv"


# =====================================================
# CARREGA DADOS
# =====================================================

print("Lendo resultados da LLM...")

with open(LLM_FILE, encoding="utf8") as f:
    llm_results = json.load(f)

print(f"PRs LLM: {len(llm_results)}")

print("Lendo issues do SonarQube...")

sonar = pd.read_csv(SONAR_FILE)

sonar = sonar[
    ["repo", "pr_number", "rule"]
].copy()

sonar["pr_number"] = sonar["pr_number"].astype(int)

sonar["rule"] = (
    sonar["rule"]
    .astype(str)
    .str.strip()
)

# Remove repetições da mesma regra na mesma PR
sonar = sonar.drop_duplicates(
    subset=["repo", "pr_number", "rule"]
)


# =====================================================
# REGRAS DA LLM
# =====================================================

llm_rules = {}

for pr in llm_results:

    chave_pr = (
        pr["repo"],
        int(pr["pr_number"])
    )

    if chave_pr not in llm_rules:
        llm_rules[chave_pr] = {}

    for item in pr.get(
        "sonarqube_rules_discussed",
        []
    ):

        rule = str(
            item["rule"]
        ).strip()

        # Se a mesma regra aparecer várias vezes,
        # mantemos apenas uma entrada.
        if rule not in llm_rules[chave_pr]:

            evidencias = item.get(
                "evidence",
                []
            )

            comentarios = []

            for evidence in evidencias:

                comentarios.append(
                    evidence.get(
                        "comment",
                        ""
                    )
                )

            llm_rules[chave_pr][rule] = {

                "mentioned":
                    item["mentioned"],

                "mention_type":
                    item["mention_type"],

                "relationship":
                    item["relationship"],

                "discussion":
                    " | ".join(
                        c for c in comentarios
                        if c
                    )

            }


# =====================================================
# COMPARAÇÃO SONARQUBE × LLM
# =====================================================

resultados = []

for _, row in sonar.iterrows():

    repo = row["repo"]

    pr_number = int(
        row["pr_number"]
    )

    rule = row["rule"]

    chave_pr = (
        repo,
        pr_number
    )

    regra_llm = (
        llm_rules
        .get(chave_pr, {})
        .get(rule)
    )

    if regra_llm is None:

        resultados.append({

            "repo": repo,

            "pr_number": pr_number,

            "sonarqube_rule": rule,

            "llm_mentioned": False,

            "mention_type":
                "NOT_APPLICABLE",

            "relationship":
                "NOT_DISCUSSED",

            "discussion":
                ""

        })

    else:

        resultados.append({

            "repo": repo,

            "pr_number": pr_number,

            "sonarqube_rule": rule,

            "llm_mentioned":
                regra_llm["mentioned"],

            "mention_type":
                regra_llm["mention_type"],

            "relationship":
                regra_llm["relationship"],

            "discussion":
                regra_llm["discussion"]

        })


resultado = pd.DataFrame(
    resultados
)


# =====================================================
# SALVA TABELA DETALHADA
# =====================================================

resultado.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# =====================================================
# ESTATÍSTICAS
# =====================================================

print()
print("=" * 70)
print("RQ5 - SONARQUBE × LLM")
print("=" * 70)

print()
print(
    f"PRs finais analisados : "
    f"{len(llm_results)}"
)

print(
    f"PR + regra únicos    : "
    f"{len(resultado)}"
)

print()
print("Relacionamentos:")

contagem = (
    resultado["relationship"]
    .value_counts()
)

print(
    contagem.to_string()
)

print()
print("Percentuais:")

percentuais = (
    resultado["relationship"]
    .value_counts(
        normalize=True
    ) * 100
)

for categoria, percentual in percentuais.items():

    print(
        f"{categoria:20s}: "
        f"{percentual:.2f}%"
    )

print()
print("=" * 70)

print(
    f"\nArquivo salvo em: "
    f"{OUTPUT_FILE}"
)