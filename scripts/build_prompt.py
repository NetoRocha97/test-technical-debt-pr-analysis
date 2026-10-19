
"""
build_prompt.py

Utilities for constructing the messages sent to the LLM.
"""

from pathlib import Path
from typing import Any


# =====================================================
# PROMPT RESOURCES
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

PROMPT_FILE = BASE_DIR / "prompt_template.md"
PROTOCOL_FILE = BASE_DIR / "LLM_ANALYSIS_PROTOCOL.md"


def load_prompt_template() -> str:
    """Load the system prompt."""
    return PROMPT_FILE.read_text(encoding="utf-8")


def load_protocol() -> str:
    """Load the annotation protocol."""
    return PROTOCOL_FILE.read_text(encoding="utf-8")


# =====================================================
# FORMATTING
# =====================================================

def format_review_threads(pr: dict[str, Any]) -> str:

    lines = []

    if not pr.get("review_threads"):
        return "None"

    for thread in pr["review_threads"]:

        lines.append("-" * 60)
        lines.append(f"Thread ID: {thread['thread_id']}")
        lines.append(f"File: {thread['path']}")
        lines.append(f"Line: {thread['line']}")
        lines.append("")

        for comment in thread["comments"]:

            lines.append(f"Author: {comment['author']}")
            lines.append(f"Date: {comment['created_at']}")
            lines.append(comment["body"])
            lines.append("")

    return "\n".join(lines)


def format_issue_comments(pr: dict[str, Any]) -> str:

    lines = []

    if not pr.get("issue_comments"):
        return "None"

    for comment in pr["issue_comments"]:

        lines.append(f"Author: {comment['author']}")
        lines.append(f"Date: {comment['created_at']}")
        lines.append(comment["body"])
        lines.append("")

    return "\n".join(lines)


# =====================================================
# USER MESSAGE
# =====================================================

def build_user_message(pr: dict[str, Any]) -> str:

    text = f"""
# Pull Request

Repository:
{pr["repo"]}

Pull Request Number:
{pr["pr_number"]}

Title:
{pr.get("title", "")}

Description:
{pr.get("description", "")}

# Review Threads

{format_review_threads(pr)}

# Issue Comments

{format_issue_comments(pr)}
"""

    sonar_rules = pr.get("sonar_rules", [])

    if sonar_rules:

        text += "\n# SonarQube Issues\n"

        for idx, issue in enumerate(sonar_rules, start=1):

            text += f"""

Issue {idx}

Rule:
{issue.get("rule", "")}

Severity:
{issue.get("severity", "")}

Type:
{issue.get("type", "")}

Status:
{issue.get("status", "")}

File:
{issue.get("file", "")}

Message:
{issue.get("message", "")}
"""

    else:

        text += "\n# SonarQube Issues\n\nNone"

    return text.strip()


# =====================================================
# MESSAGE CONSTRUCTION
# =====================================================

def build_messages(pr: dict[str, Any]) -> list[dict[str, str]]:

    return [

        {
            "role": "system",
            "content": load_prompt_template(),
        },

        {
            "role": "system",
            "content": load_protocol(),
        },

        {
            "role": "user",
            "content": build_user_message(pr),
        },

    ]
