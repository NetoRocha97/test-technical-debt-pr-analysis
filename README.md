# Test Technical Debt in Pull Request Discussions

This repository contains the scripts and supporting artifacts used in the empirical study of Test Technical Debt (Test TD) discussions in pull requests (PRs) from Apache Java projects. The repository supports PR data collection, LLM-assisted classification, manual validation, and the generation of descriptive results for RQ1–RQ5.

The scripts represent more than one stage/version of the analysis. In particular, scripts `03`–`06` operate on a thread-level result structure, whereas scripts `10`–`14` read the later PR-level file `data/llm_results_final.json`. Therefore, the numbered scripts should not be interpreted as one uninterrupted execution sequence. Follow the workflow that corresponds to the artifacts you intend to reproduce.

## Repository organization

```text
.
├── data/
│   ├── prs_unicos.csv
│   ├── filtered_test_processed_issues.csv
│   ├── prs_dataset*.json
│   ├── llm_results*.json
│   ├── prs_rejected.json
│   └── rejection_reasons.json
├── results/
│   ├── rq1/
│   ├── rq2/
│   ├── rq3/
│   ├── rq4/
│   └── rq5/
├── scripts/
│   ├── 01_collect_prs.py
│   ├── 02_analyze_llm.py
│   ├── 03_validate_results.py
│   ├── 04_generate_statistics.py
│   ├── 05_export_results.py
│   ├── 06_prepare_manual_validation.py
│   ├── 07_generate_comparison_spreadsheet.py
│   ├── 08_create_remaining_dataset.py
│   ├── 09_merge_results.py
│   ├── 10_rq1_statistics.py
│   ├── 11_rq2_statistics.py
│   ├── 12_rq3_statistics.py
│   ├── 13_rq4_statistics.py
│   ├── 14_rq5_statistics.py
│   ├── analyze_rejections.py
│   ├── build_prompt.py
│   ├── prompt_rejection.py
│   ├── schema.py
│   └── schema_rejection.py
├── LLM_ANALYSIS_PROTOCOL.md
└── README.md
```

The exact files available in `data/` and `results/` depend on the version of the dataset and on which stages have already been executed. The JSON/CSV/XLSX artifacts are inputs to later stages as well as outputs of earlier stages.

## Requirements

- Python 3.10 or later is recommended. The scripts use standard Python libraries and the third-party packages listed below; the repository does not currently pin exact package versions.
- Internet access is required for GitHub API collection and OpenAI API analysis.
- A GitHub personal access token is recommended for collection to increase the GitHub API rate limit.
- An OpenAI API key is required only when running the LLM classification scripts.

Install the Python dependencies from the repository root:

```bash
python -m pip install pandas openai matplotlib openpyxl
```

Set credentials as environment variables before running the corresponding stages.

Linux/macOS:

```bash
export GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

Windows PowerShell:

```powershell
$env:GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
$env:OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```

Do not commit API keys to the repository.

## Reproducing the statistical results from the provided analysis artifacts

This is the shortest route when the goal is to regenerate the RQ tables, charts, and text summaries without recollecting PRs or rerunning the LLM. Run commands from the repository root.

First, place the required input files in the `data/` directory:

- `llm_results_final.json` — final PR-level LLM classifications used by RQ1, RQ2, and RQ4, and as the LLM input for RQ5.
- `rejection_reasons.json` — rejection-reason classifications used by RQ3.
- `filtered_test_processed_issues.csv` — SonarQube issue data used by RQ5.

Then run:

```bash
python scripts/10_rq1_statistics.py
python scripts/11_rq2_statistics.py
python scripts/12_rq3_statistics.py
python scripts/13_rq4_statistics.py
python scripts/14_rq5_statistics.py
```

The scripts create their output directories when needed and write the generated artifacts under `results/`:

| Script | Input files | Main output |
|---|---|---|
| `10_rq1_statistics.py` | `data/llm_results_final.json` | `results/rq1/` — summary tables, charts, and text results |
| `11_rq2_statistics.py` | `data/llm_results_final.json` | `results/rq2/` — suggestion, agreement, and resolution summaries, tables, and charts |
| `12_rq3_statistics.py` | `data/rejection_reasons.json` | `results/rq3/` — rejection-reason tables, charts, and text results |
| `13_rq4_statistics.py` | `data/llm_results_final.json` | `results/rq4/` — Test TD type, agreement, and resolution summaries and cross-tabulations |
| `14_rq5_statistics.py` | `data/llm_results_final.json`, `data/filtered_test_processed_issues.csv` | `results/rq5_sonarqube_comparison.csv` — SonarQube/LLM comparison |

The RQ3 script does not derive rejection reasons from `llm_results_final.json`; it specifically reads `rejection_reasons.json`. The RQ5 script expects the CSV to contain at least the columns `repo`, `pr_number`, and `rule`.

## Data collection

`01_collect_prs.py` collects PR metadata, review comments, issue comments, reconstructed review threads, and associated SonarQube rules. It reads:

- `data/prs_unicos.csv` — the list of repository/PR pairs to collect;
- `data/filtered_test_processed_issues.csv` — the SonarQube issue records associated with PRs.

Run:

```bash
python scripts/01_collect_prs.py
```

The script writes `data/prs_dataset.json`. It uses the GitHub REST API and the optional `GITHUB_TOKEN` environment variable.

**Important input/output naming issue:** the later dataset-preparation script `08_create_remaining_dataset.py` expects `data/prs_dataset_full.json`, not `data/prs_dataset.json`. The collection script does not rename or copy its output to that expected name. Before continuing, verify that the collected dataset is the intended full dataset and explicitly place/copy it under the expected filename, or update the relevant path in the script. Do not overwrite a different dataset without checking it.

## LLM-assisted classification and manual validation

The LLM analysis stage uses `02_analyze_llm.py`. In its current configuration, it reads `data/prs_dataset_remaining.json` and writes `data/llm_results_remaining.json`. It uses the OpenAI API with the model identifier configured in the script (`gpt-5.5`) and resumes by skipping PRs already present in its result file.

The script imports `build_prompt.py` and `schema.py`. `build_prompt.py` loads two prompt resources relative to its own directory:

- `prompt_template.md`;
- `LLM_ANALYSIS_PROTOCOL.md`.

Consequently, both resources must be available in the same directory as `build_prompt.py` (normally `scripts/`). Check this placement before execution. The protocol file included with the repository must be copied there if it is stored elsewhere. The prompt template is also required; it was not among the script/supporting files supplied for this README revision.

The current `02_analyze_llm.py` configuration is set to process the remaining dataset. To process the validation dataset instead, the commented `DATASET_FILE` and `RESULT_FILE` alternatives in the script must be selected deliberately. Do not run both configurations against the same output file.

The intended dataset split/merge utilities are:

1. `08_create_remaining_dataset.py` — compares `prs_dataset_full.json` with `prs_dataset_validation.json` and creates `prs_dataset_remaining.json`.
2. `02_analyze_llm.py` — analyzes the configured dataset and saves the LLM results incrementally.
3. `09_merge_results.py` — merges `llm_results_validation.json` and `llm_results_remaining.json` into `llm_results.json`.

Run the split and merge scripts with:

```bash
python scripts/08_create_remaining_dataset.py
python scripts/09_merge_results.py
```

Run `02_analyze_llm.py` between these commands after configuring the validation/remaining dataset selection as appropriate:

```bash
python scripts/02_analyze_llm.py
```

The split/merge workflow expects the following files to exist before it can run: `prs_dataset_full.json`, `prs_dataset_validation.json`, and (for merging) both `llm_results_validation.json` and `llm_results_remaining.json`.

### Manual validation utilities

The following scripts belong to the thread-level validation workflow:

- `06_prepare_manual_validation.py` reads `data/llm_results.json` and creates `results/Manual_Validation.csv`, with columns for LLM classifications and corresponding manual annotations.
- `07_generate_comparison_spreadsheet.py` reads `data/manual_validation.xlsx` and `data/llm_results_validation.json`, then writes `results/validação/manual_validation_with_llm.xlsx`.

The spreadsheet-generation script expects the manually completed workbook to be named `data/manual_validation.xlsx`. Ensure that the output directory `results/validação/` exists before running it; the script does not create that nested directory itself.

The scripts `03_validate_results.py`, `04_generate_statistics.py`, and `05_export_results.py` also read `data/llm_results.json`. They are associated with the earlier thread-level result format. They should only be run with a JSON file matching the structure expected by those scripts; they are not substitutes for scripts `10`–`14`, which use `llm_results_final.json`.

## Rejection-reason analysis (RQ3)

`analyze_rejections.py` performs a separate LLM classification of the reasons why rejected suggestions were not adopted. It reads `data/prs_rejected.json`, calls the OpenAI API, and incrementally writes `data/rejection_reasons.json`.

Run:

```bash
python scripts/analyze_rejections.py
```

This stage requires `OPENAI_API_KEY`, the `openai` package, and the supporting modules `prompt_rejection.py` and `schema_rejection.py`. The prompt and schema are separate from those used in the main PR classification. After this file has been generated, run `12_rq3_statistics.py` to generate the RQ3 statistics.

## Script reference

| Script | Purpose | Principal input(s) | Principal output(s) |
|---|---|---|---|
| `01_collect_prs.py` | Collect PR data and discussion from GitHub and associate SonarQube issues | `prs_unicos.csv`, `filtered_test_processed_issues.csv` | `prs_dataset.json` |
| `02_analyze_llm.py` | Classify PR discussion with an LLM | `prs_dataset_remaining.json` or configured validation dataset | `llm_results_remaining.json` or configured result file |
| `03_validate_results.py` | Validate fields and enumerated values in thread-level results | `llm_results.json` | Console validation report |
| `04_generate_statistics.py` | Generate descriptive counts for thread-level annotations | `llm_results.json` | Console statistics |
| `05_export_results.py` | Export thread-level variables for analysis | `llm_results.json` | CSV files under `results/` |
| `06_prepare_manual_validation.py` | Create a manual annotation spreadsheet in CSV format | `llm_results.json` | `results/Manual_Validation.csv` |
| `07_generate_comparison_spreadsheet.py` | Compare manual and LLM validation results | `manual_validation.xlsx`, `llm_results_validation.json` | `results/validação/manual_validation_with_llm.xlsx` |
| `08_create_remaining_dataset.py` | Separate validation PRs from the remaining dataset | `prs_dataset_full.json`, `prs_dataset_validation.json` | `prs_dataset_remaining.json` |
| `09_merge_results.py` | Merge validation and remaining LLM results | `llm_results_validation.json`, `llm_results_remaining.json` | `llm_results.json` |
| `10_rq1_statistics.py` | Generate RQ1 results | `llm_results_final.json` | `results/rq1/` |
| `11_rq2_statistics.py` | Generate RQ2 results | `llm_results_final.json` | `results/rq2/` |
| `12_rq3_statistics.py` | Generate RQ3 rejection-reason statistics | `rejection_reasons.json` | `results/rq3/` |
| `13_rq4_statistics.py` | Generate RQ4 results | `llm_results_final.json` | `results/rq4/` |
| `14_rq5_statistics.py` | Compare SonarQube rules with discussion classifications | `llm_results_final.json`, `filtered_test_processed_issues.csv` | `results/rq5_sonarqube_comparison.csv` |
| `analyze_rejections.py` | Classify why suggestions were rejected | `prs_rejected.json` | `rejection_reasons.json` |

## Reproducibility notes and current limitations

The statistical scripts can be rerun independently when their stated input artifacts are available. Reproducing the complete pipeline from raw PR identifiers requires additional care because the current scripts contain path and format differences between stages:

1. `01_collect_prs.py` writes `prs_dataset.json`, while `08_create_remaining_dataset.py` expects `prs_dataset_full.json`.
2. `build_prompt.py` expects `prompt_template.md` and `LLM_ANALYSIS_PROTOCOL.md` beside the module. The prompt template must be included in that location; the protocol file must also be placed there.
3. `03`–`06` use the earlier thread-level `llm_results.json` format. Scripts `10`, `11`, `13`, and `14` use the later PR-level `llm_results_final.json` format. These files are not interchangeable.
4. `07_generate_comparison_spreadsheet.py` writes to a nested output directory that it does not create. Create `results/validação/` before running it.
5. `12_rq3_statistics.py` depends on the separately generated `rejection_reasons.json`; it does not use the final PR-level results file directly.
6. The repository does not currently include a pinned `requirements.txt` or automated orchestration script. The dependency installation command above reflects the third-party imports found in the supplied scripts, not a tested lockfile.

For these reasons, the most reproducible route using the supplied final artifacts is the statistical workflow described above. A full rerun from GitHub collection through final RQ outputs requires checking the input files, aligning the dataset filenames and result schemas, and ensuring all prompt resources are present before execution.

## Supporting documentation

`LLM_ANALYSIS_PROTOCOL.md` documents the qualitative classification protocol used to guide the LLM analysis, including the scope, evidence requirements, and decision rules. The rejection-reason classifier uses its own prompt and JSON schema in `prompt_rejection.py` and `schema_rejection.py`.
