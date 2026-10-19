
import json

VALIDATION_FILE = "data/llm_results_validation.json"

REMAINING_FILE = "data/llm_results_remaining.json"

OUTPUT_FILE = "data/llm_results.json"


# =====================================================
# LOAD RESULTS
# =====================================================

with open(VALIDATION_FILE, encoding="utf8") as f:
    validation = json.load(f)

with open(REMAINING_FILE, encoding="utf8") as f:
    remaining = json.load(f)


# =====================================================
# MERGE AND SORT RESULTS
# =====================================================

merged_results = validation + remaining

merged_results.sort(
    key=lambda x: (
        x["repo"],
        x["pr_number"]
    )
)


# =====================================================
# SAVE MERGED RESULTS
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf8"
) as f:

    json.dump(
        merged_results,
        f,
        indent=2,
        ensure_ascii=False
    )


# =====================================================
# DISPLAY SUMMARY
# =====================================================

print()

print("=" * 60)
print("MERGED RESULTS")
print("=" * 60)

print(f"Validation : {len(validation)}")
print(f"Remaining  : {len(remaining)}")
print(f"Total      : {len(merged_results)}")


# =====================================================
# CHECK FOR DUPLICATES
# =====================================================

ids = [

    (
        pr["repo"],
        pr["pr_number"]
    )

    for pr in merged_results

]

duplicates = len(ids) - len(set(ids))

print(f"Duplicates : {duplicates}")

print("=" * 60)

if len(merged_results) == 1152 and duplicates == 0:

    print("\n✓ Final file created successfully.")

else:

    print("\n⚠ Please check the generated file.")
