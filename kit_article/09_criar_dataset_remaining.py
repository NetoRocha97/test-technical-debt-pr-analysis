import json

FULL_DATASET = "data/prs_dataset_full.json"

VALIDATION_DATASET = "data/prs_dataset_validation.json"

OUTPUT_DATASET = "data/prs_dataset_remaining.json"


with open(FULL_DATASET, encoding="utf8") as f:
    full = json.load(f)

with open(VALIDATION_DATASET, encoding="utf8") as f:
    validation = json.load(f)

validation_ids = {

    (
        pr["repo"],
        pr["pr_number"]
    )

    for pr in validation

}

remaining = [

    pr

    for pr in full

    if (

        pr["repo"],
        pr["pr_number"]

    ) not in validation_ids

]

with open(
    OUTPUT_DATASET,
    "w",
    encoding="utf8"
) as f:

    json.dump(

        remaining,

        f,

        indent=2,

        ensure_ascii=False

    )

print()

print("=" * 50)

print(f"Dataset completo : {len(full)}")

print(f"Validação        : {len(validation)}")

print(f"Restantes        : {len(remaining)}")

print("=" * 50)