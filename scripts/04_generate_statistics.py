
import json
from collections import Counter

RESULT_FILE = "data/llm_results.json"


# =====================================================
# STATISTICS HELPER
# =====================================================

def print_counter(title, counter):

    print(f"\n{title}")
    print("-" * len(title))

    total = sum(counter.values())

    for key, value in counter.most_common():

        percentage = 0

        if total > 0:
            percentage = value / total * 100

        print(f"{key:25} {value:5} ({percentage:5.1f}%)")


# =====================================================
# MAIN EXECUTION
# =====================================================

def main():

    with open(RESULT_FILE, encoding="utf8") as f:
        prs = json.load(f)

    objective_counter = Counter()
    scope_counter = Counter()
    td_counter = Counter()
    category_counter = Counter()
    suggestion_counter = Counter()
    suggestion_type_counter = Counter()
    suggestion_author_counter = Counter()
    code_suggestion_counter = Counter()
    agreement_counter = Counter()
    resolution_counter = Counter()
    rejection_counter = Counter()
    convergence_counter = Counter()
    divergence_counter = Counter()
    novelty_counter = Counter()
    rules_counter = Counter()

    total_threads = 0
    prs_with_td = 0

    for pr in prs:

        objective_counter[pr["primary_pr_objective"]] += 1

        if pr["contains_test_td_discussion"] == "YES":
            prs_with_td += 1

        for thread in pr["threads"]:

            total_threads += 1

            scope_counter[thread["scope"]] += 1

            td_counter[thread["test_td_discussion"]] += 1

            category_counter[
                thread["test_td_category"]
            ] += 1

            suggestion_counter[
                thread["contains_suggestion"]
            ] += 1

            suggestion_type_counter[
                thread["suggestion_type"]
            ] += 1

            suggestion_author_counter[
                thread["suggestion_author"]
            ] += 1

            code_suggestion_counter[
                thread["contains_code_suggestion"]
            ] += 1

            agreement_counter[
                thread["agreement"]
            ] += 1

            resolution_counter[
                thread["resolution"]
            ] += 1

            rejection_counter[
                thread["rejection_reason"]
            ] += 1

            convergence_counter[
                thread["convergence"]["classification"]
            ] += 1

            divergence_counter[
                thread["divergence"]["classification"]
            ] += 1

            novelty_counter[
                thread["novelty"]["classification"]
            ] += 1

            for rule in thread["convergence"]["related_rules"]:

                rules_counter[
                    rule["rule"]
                ] += 1

    print("\n===================================================")
    print("GENERAL")
    print("===================================================")

    print(f"Analyzed PRs                : {len(prs)}")
    print(f"PRs with Test TD            : {prs_with_td}")
    print(f"Analyzed threads            : {total_threads}")

    print("\n===================================================")
    print("RQ1")
    print("Maintenance objectives")
    print("===================================================")

    print_counter(
        "Primary PR Objective",
        objective_counter
    )

    print("\n===================================================")
    print("RQ2")
    print("Characteristics of suggestions")
    print("===================================================")

    print_counter(
        "Scope",
        scope_counter
    )

    print_counter(
        "Test TD Discussion",
        td_counter
    )

    print_counter(
        "Test TD Category",
        category_counter
    )

    print_counter(
        "Contains Suggestion",
        suggestion_counter
    )

    print_counter(
        "Suggestion Type",
        suggestion_type_counter
    )

    print_counter(
        "Suggestion Author",
        suggestion_author_counter
    )

    print_counter(
        "Contains Code Suggestion",
        code_suggestion_counter
    )

    print_counter(
        "Agreement",
        agreement_counter
    )

    print_counter(
        "Resolution",
        resolution_counter
    )

    print("\n===================================================")
    print("RQ3")
    print("Reasons for rejection")
    print("===================================================")

    print_counter(
        "Rejection Reason",
        rejection_counter
    )

    print("\n===================================================")
    print("RQ4")
    print("Comparison with SonarQube")
    print("===================================================")

    print_counter(
        "Convergence",
        convergence_counter
    )

    print_counter(
        "Divergence",
        divergence_counter
    )

    print_counter(
        "Novelty",
        novelty_counter
    )

    print_counter(
        "Related SonarQube Rules",
        rules_counter
    )


if __name__ == "__main__":
    main()
