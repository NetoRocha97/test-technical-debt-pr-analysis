
import json

from schema import ANALYSIS_SCHEMA

RESULT_FILE = "data/llm_results.json"


# =====================================================
# VALIDATION HELPERS
# =====================================================

def validate_enum(value, allowed_values, field):

    if value not in allowed_values:
        raise ValueError(
            f"{field}: invalid value -> {value}"
        )


# =====================================================
# THREAD VALIDATION
# =====================================================

def validate_thread(thread):

    validate_enum(
        thread["scope"],
        [
            "TEST",
            "PRODUCTION",
            "MIXED",
            "UNKNOWN"
        ],
        "scope"
    )

    validate_enum(
        thread["test_td_discussion"],
        [
            "YES",
            "NO",
            "UNCERTAIN"
        ],
        "test_td_discussion"
    )

    validate_enum(
        thread["test_td_category"],
        [
            "Assertion",
            "Exception Handling",
            "Test Failure",
            "Test Fragility",
            "Test Maintainability",
            "Test Readability",
            "Test Design",
            "Test Execution",
            "Test Smell",
            "Test Fixture",
            "Test Dependency",
            "Test Data",
            "Test Duplication",
            "Test Refactoring",
            "Other",
            "UNKNOWN"
        ],
        "test_td_category"
    )

    validate_enum(
        thread["contains_suggestion"],
        [
            "YES",
            "NO"
        ],
        "contains_suggestion"
    )

    validate_enum(
        thread["suggestion_type"],
        [
            "EXPLICIT",
            "IMPLICIT",
            "NONE",
            "UNKNOWN"
        ],
        "suggestion_type"
    )

    validate_enum(
        thread["agreement"],
        [
            "AGREED",
            "REJECTED",
            "POSTPONED",
            "IGNORED",
            "UNKNOWN"
        ],
        "agreement"
    )

    validate_enum(
        thread["resolution"],
        [
            "FIXED",
            "P-FIXED",
            "UNFIXED",
            "UNKNOWN"
        ],
        "resolution"
    )

    if not (0 <= thread["confidence"] <= 1):
        raise ValueError(
            f"Invalid confidence: {thread['confidence']}"
        )


# =====================================================
# PULL REQUEST VALIDATION
# =====================================================

def validate_pr(pr):

    required_fields = ANALYSIS_SCHEMA["required"]

    for field in required_fields:

        if field not in pr:

            raise ValueError(
                f"Missing field: {field}"
            )

    for thread in pr["threads"]:

        validate_thread(thread)


# =====================================================
# MAIN EXECUTION
# =====================================================

def main():

    with open(
        RESULT_FILE,
        encoding="utf8"
    ) as f:

        results = json.load(f)

    print()

    print(f"Analyzed PRs: {len(results)}")

    errors = 0

    for pr in results:

        try:

            validate_pr(pr)

        except Exception as e:

            errors += 1

            print()

            print(
                f"{pr['repo']} #{pr['pr_number']}"
            )

            print(e)

    print()

    if errors == 0:

        print("All results are valid.")

    else:

        print(f"{errors} error(s) found.")


if __name__ == "__main__":

    main()
