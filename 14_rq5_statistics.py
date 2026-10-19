
import json
import pandas as pd

LLM_FILE = "data/llm_results_final.json"
SONAR_FILE = "data/filtered_test_processed_issues.csv"

OUTPUT_FILE = "results/rq5_sonarqube_comparison.csv"


# =====================================================
# LOAD DATA
# =====================================================

print("Loading LLM results...")

with open(LLM_FILE, encoding="utf8") as file:
    llm_results = json.load(file)

print(f"LLM PRs: {len(llm_results)}")

print("Loading SonarQube issues...")

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

# Remove duplicate occurrences of the same rule within a PR
sonar = sonar.drop_duplicates(
    subset=["repo", "pr_number", "rule"]
)


# =====================================================
# LLM RULES
# =====================================================

llm_rules = {}

for pr in llm_results:

    pr_key = (
        pr["repo"],
        int(pr["pr_number"])
    )

    if pr_key not in llm_rules:
        llm_rules[pr_key] = {}

    for item in pr.get(
        "sonarqube_rules_discussed",
        []
    ):

        rule = str(
            item["rule"]
        ).strip()

        # Keep only one entry when the same rule appears multiple times
        if rule not in llm_rules[pr_key]:

            evidence_items = item.get(
                "evidence",
                []
            )

            comments = []

            for evidence in evidence_items:

                comments.append(
                    evidence.get(
                        "comment",
                        ""
                    )
                )

            llm_rules[pr_key][rule] = {

                "mentioned":
                    item["mentioned"],

                "mention_type":
                    item["mention_type"],

                "relationship":
                    item["relationship"],

                "discussion":
                    " | ".join(
                        comment for comment in comments
                        if comment
                    )

            }


# =====================================================
# SONARQUBE × LLM COMPARISON
# =====================================================

results = []

for _, row in sonar.iterrows():

    repo = row["repo"]

    pr_number = int(
        row["pr_number"]
    )

    rule = row["rule"]

    pr_key = (
        repo,
        pr_number
    )

    llm_rule = (
        llm_rules
        .get(pr_key, {})
        .get(rule)
    )

    if llm_rule is None:

        results.append({

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

        results.append({

            "repo": repo,

            "pr_number": pr_number,

            "sonarqube_rule": rule,

            "llm_mentioned":
                llm_rule["mentioned"],

            "mention_type":
                llm_rule["mention_type"],

            "relationship":
                llm_rule["relationship"],

            "discussion":
                llm_rule["discussion"]

        })


result = pd.DataFrame(
    results
)


# =====================================================
# SAVE DETAILED TABLE
# =====================================================

result.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# =====================================================
# STATISTICS
# =====================================================

print()
print("=" * 70)
print("RQ5 - SONARQUBE × LLM")
print("=" * 70)

print()
print(
    f"Final PRs analyzed    : "
    f"{len(llm_results)}"
)

print(
    f"Unique PR-rule pairs  : "
    f"{len(result)}"
)

print()
print("Relationships:")

counts = (
    result["relationship"]
    .value_counts()
)

print(
    counts.to_string()
)

print()
print("Percentages:")

percentages = (
    result["relationship"]
    .value_counts(
        normalize=True
    ) * 100
)

for category, percentage in percentages.items():

    print(
        f"{category:20s}: "
        f"{percentage:.2f}%"
    )

print()
print("=" * 70)

print(
    f"\nFile saved to: "
    f"{OUTPUT_FILE}"
)
