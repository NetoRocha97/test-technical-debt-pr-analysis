import csv
import json
from pathlib import Path

RESULT_FILE = "data/llm_results.json"

OUTPUT_DIR = Path("results")

OUTPUT_FILE = OUTPUT_DIR / "Manual_Validation.csv"


def carregar_resultados():

    with open(
        RESULT_FILE,
        encoding="utf8"
    ) as f:

        return json.load(f)


def main():

    OUTPUT_DIR.mkdir(exist_ok=True)

    prs = carregar_resultados()

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([

            "Repository",
            "PR",
            "ThreadID",

            "LLM_Scope",
            "Manual_Scope",

            "LLM_TestTDDiscussion",
            "Manual_TestTDDiscussion",

            "LLM_TestTDCategory",
            "Manual_TestTDCategory",

            "LLM_ContainsSuggestion",
            "Manual_ContainsSuggestion",

            "LLM_SuggestionType",
            "Manual_SuggestionType",

            "LLM_Agreement",
            "Manual_Agreement",

            "LLM_Resolution",
            "Manual_Resolution",

            "LLM_RejectionReason",
            "Manual_RejectionReason",

            "LLM_Convergence",
            "Manual_Convergence",

            "LLM_Divergence",
            "Manual_Divergence",

            "LLM_Novelty",
            "Manual_Novelty",

            "Reviewer",

            "Comments"

        ])

        for pr in prs:

            for thread in pr["threads"]:

                writer.writerow([

                    pr["repo"],

                    pr["pr_number"],

                    thread["thread_id"],

                    thread["scope"],
                    "",

                    thread["test_td_discussion"],
                    "",

                    thread["test_td_category"],
                    "",

                    thread["contains_suggestion"],
                    "",

                    thread["suggestion_type"],
                    "",

                    thread["agreement"],
                    "",

                    thread["resolution"],
                    "",

                    thread["rejection_reason"],
                    "",

                    thread["convergence"]["classification"],
                    "",

                    thread["divergence"]["classification"],
                    "",

                    thread["novelty"]["classification"],
                    "",

                    "",

                    ""

                ])

    print()
    print("======================================")
    print("MANUAL VALIDATION FILE CREATED")
    print("======================================")
    print()
    print(f"File: {OUTPUT_FILE}")
    print()
    print("Fill only the columns starting with 'Manual_'.")
    print("The 'LLM_' columns must not be modified.")


if __name__ == "__main__":

    main()