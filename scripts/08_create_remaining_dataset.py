
import json

FULL_DATASET = "data/prs_dataset_full.json"

VALIDATION_DATASET = "data/prs_dataset_validation.json"

OUTPUT_DATASET = "data/prs_dataset_remaining.json"


# =====================================================
# LOAD DATASETS
# =====================================================

with open(FULL_DATASET, encoding="utf8") as f:
    full_dataset = json.load(f)

with open(VALIDATION_DATASET, encoding="utf8") as f:
    validation_dataset = json.load(f)


# =====================================================
# IDENTIFY REMAINING PULL REQUESTS
# =====================================================

validation_ids = {

    (
        pr["repo"],
        pr["pr_number"]
    )

    for pr in validation_dataset

}

remaining_dataset = [

    pr

    for pr in full_dataset

    if (

        pr["repo"],
        pr["pr_number"]

    ) not in validation_ids

]


# =====================================================
# SAVE REMAINING DATASET
# =====================================================

with open(
    OUTPUT_DATASET,
    "w",
    encoding="utf8"
) as f:

    json.dump(
        remaining_dataset,
        f,
        indent=2,
        ensure_ascii=False
    )


# =====================================================
# DISPLAY DATASET SUMMARY
# =====================================================

print()

print("=" * 50)

print(f"Full dataset      : {len(full_dataset)}")

print(f"Validation dataset: {len(validation_dataset)}")

print(f"Remaining dataset : {len(remaining_dataset)}")

print("=" * 50)
