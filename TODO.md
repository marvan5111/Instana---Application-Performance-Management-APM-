# TODO for v1.2.0 Implementation

## 1. Website Monitoring
- [x] Add generator functions to `instana_synthetic/generators.py` for website_config, website_catalog, website_metrics, website_analyze
- [x] Create `scripts/generate_website_config.py` to generate `website_config.jsonl`
- [x] Create `scripts/generate_website_catalog.py` to generate `website_catalog.jsonl`
- [x] Create `scripts/generate_website_metrics.py` to generate `website_metrics.jsonl`
- [x] Create `scripts/generate_website_analyze.py` to generate `website_analyze.jsonl`

## 2. Logging
- [x] Add generator function to `instana_synthetic/generators.py` for logs
- [x] Create `scripts/generate_logs.py` to generate `logs.jsonl`

## 3. Synthetic Checks
- [x] Add generator functions to `instana_synthetic/generators.py` for synthetic_checks and synthetic_runs
- [x] Create `scripts/generate_synthetic_checks.py` to generate `synthetic_checks.jsonl`
- [x] Create `scripts/generate_synthetic_runs.py` to generate `synthetic_runs.jsonl`

## 4. Update Validation
- [x] Update `validate_all.py` to include validation for new JSONL files
- [x] Add cross-file consistency checks for new files

## 5. Update Documentation
- [x] Update `README_INSTANA.md` to add “v1.2.0 in progress” section with checklist link and planned files
- [x] Update `v1.2.0_CHECKLIST.md` to mark completed items

## 6. Integration
- [x] Update `scripts/generate_instana_all.py` to include new generators
- [x] Test generation and validation
