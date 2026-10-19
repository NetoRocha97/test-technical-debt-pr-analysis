
import json
import time
from pathlib import Path
import os

from openai import OpenAI

from build_prompt import build_messages
from schema import RESPONSE_FORMAT

# =====================================================
# CONFIGURATION
# =====================================================

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-5.5"

client = OpenAI(api_key=API_KEY)

DATASET_FILE = "data/prs_dataset_remaining.json"
# DATASET_FILE = "data/prs_dataset_validation.json"

RESULT_FILE = "data/llm_results_remaining.json"
# RESULT_FILE = "data/llm_results_validation.json"


# =====================================================
# DATASET LOADING
# =====================================================

def load_dataset():

    with open(DATASET_FILE, encoding="utf8") as f:
        return json.load(f)


# =====================================================
# RESULTS MANAGEMENT
# =====================================================

def load_results():

    if Path(RESULT_FILE).exists():

        with open(RESULT_FILE, encoding="utf8") as f:
            return json.load(f)

    return []


def save_results(results):

    with open(
        RESULT_FILE,
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )


# =====================================================
# REVIEW COMMENT FORMATTING
# =====================================================

def format_review_threads(pr):

    lines = []

    if len(pr["review_threads"]) == 0:
        return "None"

    for thread in pr["review_threads"]:

        lines.append("-" * 60)
        lines.append(
            f"Thread: {thread['thread_id']} | "
            f"File: {thread['path']} | "
            f"Line: {thread['line']}"
        )

        for comment in thread["comments"]:

            lines.append(
                f"{comment['author']} ({comment['created_at']}):"
            )

            lines.append(comment["body"])
            lines.append("")

    return "\n".join(lines)


# =====================================================
# LLM-BASED PULL REQUEST ANALYSIS
# =====================================================

def analyze_pr(pr):

    comments = format_review_threads(pr)

    if pr["issue_comments"]:

        comments += "\n\n# Issue Comments\n\n"

        for comment in pr["issue_comments"]:

            comments += (
                f"{comment['author']} ({comment['created_at']}):\n"
            )

            comments += comment["body"]
            comments += "\n\n"

    pr_for_llm = pr.copy()
    pr_for_llm["comments"] = comments

    messages = build_messages(pr_for_llm)

    for attempt in range(3):

        try:

            response = client.responses.create(
                model=MODEL,
                input=messages,
                text={
                    "format": RESPONSE_FORMAT
                }
            )

            return json.loads(response.output_text)

        except Exception as e:

            print(f"Attempt {attempt + 1}/3 failed.")
            print(e)

            time.sleep(3)

    return None


# =====================================================
# MAIN EXECUTION
# =====================================================

def main():

    dataset = load_dataset()
    results = load_results()

    processed_prs = {
        (result["repo"], result["pr_number"])
        for result in results
    }

    total = len(dataset)

    print(f"Dataset: {total} pull request(s)")
    print(f"Existing results: {len(results)}")

    for i, pr in enumerate(dataset, start=1):

        key = (
            pr["repo"],
            pr["pr_number"]
        )

        if key in processed_prs:
            continue

        print(f"\n[{i}/{total}] {pr['repo']} #{pr['pr_number']}")

        result = analyze_pr(pr)

        if result is None:
            print("Analysis failed.")
            continue

        results.append(result)
        save_results(results)

        print("Analysis completed successfully.")

        time.sleep(1)

    print("\nProcessing completed.")


if __name__ == "__main__":
    main()
