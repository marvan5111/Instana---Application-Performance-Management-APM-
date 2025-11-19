# Release Notes: v1.2.0-instana-synthetic

## Overview
This release introduces comprehensive website monitoring, logging, and synthetic checks to the Instana APM Synthetic Data Generator, expanding coverage to 16 datasets with full validation and cross-file consistency. All new features have been thoroughly tested for integration and edge cases, ensuring production-ready synthetic data for prototyping, testing, and development workflows.

## New Features

### 🌐 Website Monitoring
- **Website Configurations** (`website_config.jsonl`): Synthetic website definitions with realistic URLs, check intervals, and performance thresholds.
- **Website Catalogs** (`website_catalog.jsonl`): Metadata catalogs for monitored websites, including labels, tags, and monitoring settings.
- **Website Metrics** (`website_metrics.jsonl`): Time-series performance metrics such as response times, availability percentages, and error rates.
- **Website Analyze** (`website_analyze.jsonl`): Detailed analysis snapshots with traces, issues, and performance insights for website monitoring.

### 📝 Logging
- **Log Entries** (`logs.jsonl`): Synthetic log data with timestamps, severity levels (INFO, WARN, ERROR), messages, and tags. Includes correlation IDs linking logs to traces and issues for realistic debugging scenarios.
- Supports multiple log sources (applications, infrastructure) with temporal consistency across datasets.

### 🔍 Synthetic Monitoring (Synthetic Checks)
- **Synthetic Checks** (`synthetic_checks.jsonl`): Definitions for API and browser-based synthetic checks, including configurations, endpoints, and thresholds.
- **Synthetic Runs** (`synthetic_runs.jsonl`): Execution results with timestamps, response times, success/failure status, and alert correlations for failed checks.
- Checks are linked to valid endpoints (e.g., monitoring "POST /checkout") with realistic failure patterns.

## Validation & Quality Assurance
- **16 Datasets Validated**: Comprehensive validation across all 16 files (10 original + 6 new) with zero errors.
- **Cross-File Consistency**: Entity IDs, correlation IDs, and references are fully consistent; no orphaned data.
- **Integration Testing**: All new datasets pass integration tests, ensuring seamless compatibility with existing workflows.
- **Edge Case Coverage**: Extensive edge case testing for realistic failure modes, temporal alignment, and data integrity.

## Technical Improvements
- Enhanced validation script (`validate_all.py`) to include new datasets and stricter consistency checks.
- Improved logging and monitoring runners (`logger.py`, `monitor_runner.py`, `synthetic_runner.py`) for better observability.
- Updated README_INSTANA.md with v1.2.0 highlights and usage examples.

## Usage Examples
Generate fresh data with new features:
```bash
python scripts/generate_instana_all.py --seed 42 --entities 120 --apps 15 --services 40 --issues 30
python validate_all.py
```

Load and inspect new datasets:
```python
import json

# Website metrics
with open("data/instana/website_metrics.jsonl") as f:
    for line in f:
        record = json.loads(line)
        print(f"Website: {record['entity_id']}, Response Time: {record['metrics']['response_time_ms']}ms")

# Synthetic check runs
with open("data/instana/synthetic_runs.jsonl") as f:
    for line in f:
        record = json.loads(line)
        print(f"Check: {record['check_id']}, Status: {record['status']}, Duration: {record['duration_ms']}ms")
```

## Breaking Changes
None. All changes are additive and backward-compatible.

## Known Issues
- Mobile monitoring (planned for future release) is not yet included.
- Visualization examples are in roadmap for v1.3.0.

## Acknowledgments
Thanks to the community for feedback on v1.1.0. This release builds on user requests for expanded monitoring capabilities.

## Download
Download the complete dataset from the [GitHub Releases](https://github.com/marvan5111/Instana---Application-Performance-Management-APM-/releases/tag/v1.2.0-instana-synthetic) page, including validation logs and sample outputs.
