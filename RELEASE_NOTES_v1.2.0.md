 # Release Notes: v1.2.0 - Expanded Data Ecosystem
 
 ## Overview
 
 Version 1.2.0 represents a massive expansion of the synthetic data ecosystem, building on the foundational datasets from v1.0.0 and v1.1.0. This release introduces comprehensive data generation capabilities for four new, critical monitoring domains: Website Monitoring, Mobile Monitoring, Logging, and advanced Synthetic Checks.
 
 With these additions, the platform can now simulate a much wider range of real-world monitoring scenarios, providing the necessary data to build and test the full-featured dashboards and alerting systems planned for v1.3.0.
 
 ## ✅ Key Features Delivered
 
 This release adds over 10 new datasets, all fully integrated into the generation and validation pipelines.
 
 1.  **Website Monitoring**
     -   `website_config.jsonl`: Generates configurations for website uptime and performance checks.
     -   `website_catalog.jsonl`: A catalog of monitored websites.
     -   `website_metrics.jsonl`: Time-series data for website response times.
     -   `website_analyze.jsonl`: Detailed analysis snapshots for website performance.
 
 2.  **Mobile Monitoring**
     -   `mobile_config.jsonl`: Configurations for mobile apps, including crash rate and response time thresholds.
     -   `mobile_catalog.jsonl`: A catalog of monitored iOS and Android applications.
     -   `mobile_metrics.jsonl`: Time-series data for mobile crash rates and response times.
     -   `mobile_analyze.jsonl`: Detailed analysis including battery drain and memory usage.
 
 3.  **Logging**
     -   `logs.jsonl`: Generates thousands of log entries with varying severity levels (INFO, WARN, ERROR), timestamps, and correlation IDs that link to other system events.
 
 4.  **Advanced Synthetic Checks**
     -   `synthetic_checks.jsonl`: Defines multi-step synthetic journeys (e.g., API or browser-based user flows) with specific validation criteria.
     -   `synthetic_runs.jsonl`: Produces detailed results for each synthetic check run, including success/failure status, duration, and error messages.
 
 ## ⚙️ Code Summary
 
 -   **`instana_synthetic/generators.py`**: Heavily updated with new generator functions for all the above datasets, including `gen_website_metrics`, `gen_mobile_metrics`, `gen_log_entry`, and `gen_synthetic_run`.
 -   **`scripts/`**: Added new scripts to orchestrate the generation of each new data type (e.g., `generate_website_metrics.py`, `generate_logs.py`).
 -   **`scripts/generate_instana_all.py`**: The main orchestrator was updated to include all the new v1.2.0 data generation scripts.
 -   **`validate_all.py`**: Significantly enhanced to provide validation and cross-file consistency checks for all new datasets. For example, it now ensures that every run in `synthetic_runs.jsonl` corresponds to a valid check in `synthetic_checks.jsonl`.
 
 ## 🧪 Validation Output
 
 The following is the expected output from running `python validate_all.py` against the new datasets introduced in v1.2.0.
 
 ```
 Validating website_config.jsonl...
 website_config.jsonl: Valid JSON, count: 10
 Sample website config keys: ['website_id', 'url', 'check_interval_seconds', 'timeout_ms', 'expected_status_codes', 'alert_on_failure', 'tags']
 
 Validating website_catalog.jsonl...
 website_catalog.jsonl: Valid JSON, count: 1
 Sample website catalog keys: ['websites']
 
 Validating website_metrics.jsonl...
 website_metrics.jsonl: Valid JSON, count: 10
 Sample website metrics keys: ['website_id', 'metric_name', 'aggregation', 'timeframe', 'points']
 
 Validating website_analyze.jsonl...
 website_analyze.jsonl: Valid JSON, count: 10
 Sample website analyze keys: ['website_id', 'snapshot_id', 'timestamp', 'response_time_ms', 'status_code', 'error_message']
 
 Validating logs.jsonl...
 logs.jsonl: Valid JSON, count: 1000
 Sample log keys: ['timestamp', 'severity', 'message', 'entity_id', 'correlation_id', 'tags', 'source']
 
 Validating synthetic_checks.jsonl...
 synthetic_checks.jsonl: Valid JSON, count: 20
 Sample synthetic check keys: ['check_id', 'name', 'type', 'endpoint_id', 'url', 'method', 'headers', 'body', 'expected_status', 'timeout_ms', 'frequency_seconds', 'locations']
 
 Validating synthetic_runs.jsonl...
 synthetic_runs.jsonl: Valid JSON, count: 100
 Sample synthetic run keys: ['run_id', 'check_id', 'timestamp', 'duration_ms', 'status', 'status_code', 'error_message', 'location']
 
 Cross-file consistency for synthetic checks and runs...
 All synthetic runs reference valid checks.
 
 Validating mobile_config.jsonl...
 mobile_config.jsonl: Valid JSON, count: 10
 Sample mobile config keys: ['mobile_app_id', 'platform', 'version', 'crash_threshold', 'response_time_threshold_ms', 'alert_on_crash']
 
 Validating mobile_catalog.jsonl...
 mobile_catalog.jsonl: Valid JSON, count: 1
 Sample mobile catalog keys: ['mobile_apps']
 
 Validating mobile_metrics.jsonl...
 mobile_metrics.jsonl: Valid JSON, count: 10
 Sample mobile metrics keys: ['mobile_app_id', 'metric_name', 'aggregation', 'timeframe', 'points']
 
 Validating mobile_analyze.jsonl...
 mobile_analyze.jsonl: Valid JSON, count: 10
 Sample mobile analyze keys: ['mobile_app_id', 'snapshot_id', 'timestamp', 'platform', 'version', 'crash_count', 'avg_response_time_ms']
 
 Validation complete.
 ```
 
 ## How to Use
 
 1.  **Generate Data**:
     ```bash
     python scripts/generate_instana_all.py
     ```
 
 2.  **Validate Data**:
     ```bash
     python validate_all.py
     ```
 
 ## Assets
 
 -   `instana-synthetic-v1.2.0.zip`: A zip archive containing all generated datasets for this release.
 -   `validation_log_v1.2.0.txt`: The full output log from the validation script, confirming the integrity of all new files.