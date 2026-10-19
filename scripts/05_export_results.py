
import json
import csv
from pathlib import Path

RESULT_FILE = "data/llm_results.json"
OUTPUT_DIR = Path("results")


# =====================================================
# DIRECTORY AND DATA MANAGEMENT
# =====================================================

def ensure_output_directory():
    OUTPUT_DIR.mkdir(exist_ok=True)


def load_results():
    with open(RESULT_FILE, encoding="utf8") as f:
        return json.load(f)


def save_csv(filename, header, rows):

    path = OUTPUT_DIR / filename

    with open(
        path,
        "w",
        newline="",
        encoding="utf8"
    ) as f:

        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


# =====================================================
# RQ1: MAINTENANCE OBJECTIVES
# =====================================================

def export_rq1(prs):

    rows = []

    for pr in prs:

        rows.append([
            pr["repo"],
            pr["pr_number"],
            pr["primary_pr_objective"],
            pr["contains_test_td_discussion"]
        ])

    save_csv(
        "RQ1_Objectives.csv",
        [
            "Repository",
            "PR",
            "PrimaryObjective",
            "ContainsTestTD"
        ],
        rows
    )


# =====================================================
# RQ2: CHARACTERISTICS OF SUGGESTIONS
# =====================================================

def export_rq2(prs):

    rows = []

    for pr in prs:

        for thread in pr["threads"]:

            rows.append([
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

    save_csv(
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
        rows
    )


# =====================================================
# RQ3: REASONS FOR REJECTION
# =====================================================

def export_rq3(prs):

    rows = []

    for pr in prs:

        for thread in pr["threads"]:

            if thread["agreement"] != "REJECTED":
                continue

            rows.append([
                pr["repo"],
                pr["pr_number"],
                thread["thread_id"],
                thread["test_td_category"],
                thread["suggestion_type"],
                thread["suggestion_author"],
                thread["rejection_reason"],
                thread["justification"]
            ])

    save_csv(
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
        rows
    )


# =====================================================
# RQ4: COMPARISON WITH SONARQUBE
# =====================================================

def export_rq4(prs):

    convergence = []
    divergence = []
    novelty = []

    for pr in prs:

        for thread in pr["threads"]:

            rules = []

            for rule in thread["convergence"]["related_rules"]:
                rules.append(rule["rule"])

            convergence.append([
                pr["repo"],
                pr["pr_number"],
                thread["thread_id"],
                thread["convergence"]["classification"],
                "; ".join(rules)
            ])

            divergence.append([
                pr["repo"],
                pr["pr_number"],
                thread["thread_id"],
                thread["divergence"]["classification"],
                thread["divergence"]["explanation"]
            ])

            novelty.append([
                pr["repo"],
                pr["pr_number"],
                thread["thread_id"],
                thread["novelty"]["classification"],
                thread["novelty"]["explanation"]
            ])

    save_csv(
        "RQ4_Convergence.csv",
        [
            "Repository",
            "PR",
            "Thread",
            "Classification",
            "RelatedRules"
        ],
        convergence
    )

    save_csv(
        "RQ4_Divergence.csv",
        [
            "Repository",
            "PR",
            "Thread",
            "Classification",
            "Explanation"
        ],
        divergence
    )

    save_csv(
        "RQ4_Novelty.csv",
        [
            "Repository",
            "PR",
            "Thread",
            "Classification",
            "Explanation"
        ],
        novelty
    )


# =====================================================
# ALL REVIEW THREADS
# =====================================================

def export_all_threads(prs):

    rows = []

    for pr in prs:

        for thread in pr["threads"]:

            rules = []

            for rule in thread["convergence"]["related_rules"]:
                rules.append(rule["rule"])

            rows.append([
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
                "; ".join(rules),
                thread["confidence"],
                thread["confidence_reason"]
            ])

    save_csv(
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
        rows
    )


# =====================================================
# SUMMARY REPORT
# =====================================================

def generate_summary(prs):

    total_prs = len(prs)

    total_threads = sum(
        len(pr["threads"])
        for pr in prs
    )

    prs_with_td = sum(
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
        f.write(
            f"PRs containing Test Technical Debt discussions: "
            f"{prs_with_td}\n"
        )
        f.write(f"Total review threads analyzed: {total_threads}\n")


# =====================================================
# MAIN EXECUTION
# =====================================================

def main():

    ensure_output_directory()

    prs = load_results()

    export_rq1(prs)
    export_rq2(prs)
    export_rq3(prs)
    export_rq4(prs)
    export_all_threads(prs)
    generate_summary(prs)

    print()
    print("=" * 60)
    print("EXPORT COMPLETED")
    print("=" * 60)

    print(f"\nResults folder: {OUTPUT_DIR.resolve()}")
    print("\nGenerated files:")

    files = sorted(OUTPUT_DIR.glob("*"))

    for file in files:
        print(f" - {file.name}")

    print()


if __name__ == "__main__":
    main()
