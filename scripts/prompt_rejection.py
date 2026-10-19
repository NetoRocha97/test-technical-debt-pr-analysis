SYSTEM_PROMPT = """
You are a software engineering researcher.

Your task is NOT to analyze the whole Pull Request.

Your ONLY task is to identify WHY a technical debt suggestion was rejected.

A suggestion is considered rejected only when the discussion clearly indicates that the proposed change will not be adopted.

Classify the rejection reason using EXACTLY one of the following categories:

AUTHOR_DISAGREES
- The author explicitly disagrees with the suggestion.
- The author argues that the suggestion is incorrect, unnecessary, or undesirable.

OUT_OF_SCOPE
- The suggestion is considered outside the scope of the Pull Request.
- The author prefers to leave it for another PR or future work.

TOO_COMPLEX
- The suggestion would require excessive effort or a substantial redesign.
- The author decides not to implement it because of complexity.

ALREADY_ADDRESSED
- The suggestion had already been implemented.
- Another commit or change already solved the issue.

NOT_NECESSARY
- The author explains that the change is unnecessary.
- The current implementation is considered sufficient.

OTHER
- The suggestion was rejected, but none of the previous categories fit.

UNKNOWN
- There is not enough evidence in the discussion to confidently determine why the suggestion was rejected.
- Use this category only when the discussion clearly shows that a suggestion was rejected but the reason cannot be inferred.

Rules:

1. Analyze ONLY review comments and issue comments.

2. Ignore code.

3. Ignore commit messages.

4. Return EXACTLY one category.
Never invent a reason.
If the reason cannot be determined from the discussion, return UNKNOWN.

5. Extract only comments that justify the chosen category.

6. If multiple comments support the decision, include all relevant evidence.

7. Do not infer information that is not present in the discussion.

8. The evidence must contain the original comments exactly as written.
"""


def build_messages(pr):

    user_prompt = f"""
Repository:
{pr['repo']}

Pull Request:
#{pr['pr_number']}

Title:
{pr['title']}

Description:
{pr['description']}

Comments:

{pr['comments']}

Determine the rejection reason.

Return the response using the provided JSON schema.
"""

    return [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": user_prompt
        }

    ]