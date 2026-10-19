
import json
import time
import urllib.request
import os
from collections import defaultdict

import pandas as pd

# =====================================================
# CONFIGURATION
# =====================================================

OWNER = "apache"

TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json"
}

if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

PRS_FILE = "data/prs_unicos.csv"
ISSUES_FILE = "data/filtered_test_processed_issues.csv"
OUTPUT_FILE = "data/prs_dataset.json"

# =====================================================
# HELPER FUNCTIONS
# =====================================================


def github_get(url):

    req = urllib.request.Request(
        url,
        headers=HEADERS
    )

    with urllib.request.urlopen(req) as response:

        return json.loads(
            response.read().decode()
        )


def load_data():

    prs = pd.read_csv(PRS_FILE)

    issues = pd.read_csv(ISSUES_FILE)

    return prs, issues


def fetch_pr(repo, pr_number):

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{repo}/pulls/{pr_number}"
    )

    return github_get(url)


def fetch_review_comments(repo, pr_number):

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{repo}/pulls/{pr_number}/comments"
    )

    return github_get(url)


def fetch_issue_comments(repo, pr_number):

    url = (
        f"https://api.github.com/repos/"
        f"{OWNER}/{repo}/issues/{pr_number}/comments"
    )

    return github_get(url)


# =====================================================
# REVIEW THREAD RECONSTRUCTION
# =====================================================

def build_threads(review_comments):

    comentarios = {}

    filhos = defaultdict(list)

    for c in review_comments:

        comentarios[c["id"]] = c

        if c.get("in_reply_to_id"):

            filhos[c["in_reply_to_id"]].append(c)

    threads = []

    for c in review_comments:

        # Only root comments start a thread
        if c.get("in_reply_to_id") is not None:
            continue

        thread = {
            "thread_id": c["id"],
            "path": c.get("path"),
            "line": c.get("line"),
            "start_line": c.get("start_line"),
            "side": c.get("side"),
            "commit_id": c.get("commit_id"),
            "comments": []
        }

        fila = [c]

        while fila:

            atual = fila.pop(0)

            thread["comments"].append({

                "comment_id": atual["id"],

                "author": atual["user"]["login"],

                "created_at": atual["created_at"],

                "updated_at": atual["updated_at"],

                "body": atual["body"]

            })

            respostas = filhos.get(atual["id"], [])

            respostas = sorted(
                respostas,
                key=lambda x: x["created_at"]
            )

            fila.extend(respostas)

        threads.append(thread)

    threads.sort(
        key=lambda x: (
            x["path"] or "",
            x["line"] or 0
        )
    )

    return threads


# =====================================================
# SONARQUBE
# =====================================================

def fetch_sonar_issues(repo, pr_number, issues):

    sonar = issues[
        (issues["repo"] == repo)
        & (issues["pr_number"] == pr_number)
    ]

    regras = []

    for _, r in sonar.iterrows():

        regras.append({

            "rule": r["rule"],

            "severity": r["severity"],

            "type": r["type"],

            "status": r["status"],

            "file": r["file"]

        })

    return regras


# =====================================================
# MAIN
# =====================================================

def main():

    prs, issues = load_data()

    dataset = []

    total = len(prs)

    for i, pr in prs.iterrows():

        repo = pr["repo"]
        pr_number = int(pr["pr_number"])

        print(f"[{i+1}/{total}] {repo} #{pr_number}")

        try:

            # -----------------------------
            # Pull request
            # -----------------------------

            pr_data = fetch_pr(repo, pr_number)

            # -----------------------------
            # Review comments
            # -----------------------------

            review_comments = fetch_review_comments(
                repo,
                pr_number
            )

            review_threads = build_threads(
                review_comments
            )

            # -----------------------------
            # Issue comments
            # -----------------------------

            issue_comments_raw = fetch_issue_comments(
                repo,
                pr_number
            )

            issue_comments = []

            for c in issue_comments_raw:

                issue_comments.append({

                    "comment_id": c["id"],

                    "author": c["user"]["login"],

                    "created_at": c["created_at"],

                    "updated_at": c["updated_at"],

                    "body": c["body"]

                })

            # -----------------------------
            # SonarQube
            # -----------------------------

            sonar_rules = fetch_sonar_issues(
                repo,
                pr_number,
                issues
            )

            # -----------------------------
            # Dataset entry
            # -----------------------------

            dataset.append({

                "repo": repo,

                "pr_number": pr_number,

                "title": pr_data.get("title"),

                "description": pr_data.get("body"),

                "metadata": {

                    "review_threads_count": len(review_threads),

                    "review_comments_count": len(review_comments),

                    "issue_comments_count": len(issue_comments),

                    "sonar_issues_count": len(sonar_rules)

                },

                "review_threads": review_threads,

                "issue_comments": issue_comments,

                "sonar_rules": sonar_rules

            })

            # Avoid hitting the rate limit
            time.sleep(0.2)

        except Exception as e:

            print(f"Error processing {repo} #{pr_number}: {e}")

    # -----------------------------
    # Save dataset
    # -----------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf8"
    ) as f:

        json.dump(
            dataset,
            f,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("=" * 60)
    print("Dataset created successfully!")
    print(f"PRs processed: {len(dataset)}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
