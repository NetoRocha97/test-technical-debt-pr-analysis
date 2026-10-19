
import json
import time
from pathlib import Path
import os

from openai import OpenAI

from prompt_rejection import build_messages
from schema_rejection import RESPONSE_FORMAT


# =====================================================
# CONFIGURATION
# =====================================================

API_KEY = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-5.5"

client = OpenAI(api_key=API_KEY)

DATASET_FILE = "data/prs_rejected.json"

RESULT_FILE = "data/rejection_reasons.json"


# =====================================================
# LOAD DATASET
# =====================================================

def load_dataset():

    with open(
        DATASET_FILE,
        encoding="utf8"
    ) as file:

        return json.load(file)


# =====================================================
# LOAD AND SAVE RESULTS
# =====================================================

def load_results():

    if Path(RESULT_FILE).exists():

        with open(
            RESULT_FILE,
            encoding="utf8"
        ) as file:

            return json.load(file)

    return []


def save_results(results):

    with open(
        RESULT_FILE,
        "w",
        encoding="utf8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False
        )


# =====================================================
# FORMAT COMMENTS
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

            lines.append(
                comment["body"]
            )

            lines.append("")

    return "\n".join(lines)


# =====================================================
# LLM ANALYSIS
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

    pr_llm = {

        "repo": pr["repo"],

        "pr_number": pr["pr_number"],

        "title": pr["title"],

        "description": pr["description"],

        "comments": comments

    }

    messages = build_messages(pr_llm)

    for attempt in range(3):

        try:

            response = client.responses.create(

                model=MODEL,

                input=messages,

                text={
                    "format": RESPONSE_FORMAT
                }

            )

            return json.loads(
                response.output_text
            )

        except Exception as error:

            print(
                f"Attempt {attempt + 1}/3 failed."
            )

            print(error)

            time.sleep(3)

    return None


# =====================================================
# MAIN
# =====================================================

def main():

    dataset = load_dataset()

    results = load_results()

    processed_prs = {
        (result["repo"], result["pr_number"])
        for result in results
    }

    total = len(dataset)

    print(f"Dataset: {total} PR(s)")

    print(f"Existing results: {len(results)}")

    for i, pr in enumerate(dataset, start=1):

        pr_key = (
            pr["repo"],
            pr["pr_number"]
        )

        if pr_key in processed_prs:

            continue

        print(
            f"\n[{i}/{total}] "
            f"{pr['repo']} "
            f"#{pr['pr_number']}"
        )

        result = analyze_pr(pr)

        if result is None:

            print("Failed.")

            continue

        results.append(result)

        save_results(results)

        processed_prs.add(pr_key)

        print(
            f"Reason: "
            f"{result['rejection_reason']['value']}"
        )

        print("OK")

        time.sleep(1)

    print()

    print("=" * 60)

    print("PROCESSING COMPLETED")

    print("=" * 60)

    print()

    print("Results saved to:")

    print(RESULT_FILE)

    print()

    print("=" * 60)


if __name__ == "__main__":

    main()
