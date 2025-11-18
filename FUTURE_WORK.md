# Future Work Roadmap

This document outlines planned enhancements and improvements for the Instana APM Synthetic Data Generator beyond v1.0.0.

## Priority Enhancements

### 1. Website Monitoring (v1.2.0)
**Goal:** Add synthetic website monitoring configurations, catalogs, metrics, and analyze snapshots to cover Instana's website monitoring APIs.

**Details:**
- Generate website configurations: synthetic website definitions with URLs, check intervals, and thresholds
- Create website catalogs: lists of monitored websites with metadata
- Produce website metrics: synthetic performance metrics (response times, availability, error rates)
- Simulate website analyze snapshots: detailed analysis data with traces and issues

**Acceptance Criteria:**
- `website_config.jsonl`: Valid website configurations with realistic URLs and settings
- `website_catalog.jsonl`: Catalog of websites with metadata
- `website_metrics.jsonl`: Time-series metrics for websites
- `website_analyze.jsonl`: Analysis snapshots with traces and issues
- All files pass validation and cross-file consistency

**Effort:** Medium (1–2 weeks)

---

### 2. Mobile Monitoring (v1.2.0)
**Goal:** Add synthetic mobile app monitoring configurations, catalogs, metrics, and analyze snapshots.

**Details:**
- Generate mobile app configurations: synthetic app definitions with platforms, versions, and thresholds
- Create mobile catalogs: lists of monitored apps with metadata
- Produce mobile metrics: synthetic performance metrics (crash rates, response times, user sessions)
- Simulate mobile analyze snapshots: detailed analysis with crash reports and traces

**Acceptance Criteria:**
- `mobile_config.jsonl`: Valid mobile app configurations
- `mobile_catalog.jsonl`: Catalog of mobile apps
- `mobile_metrics.jsonl`: Time-series metrics for mobile apps
- `mobile_analyze.jsonl`: Analysis snapshots with crash data
- All files pass validation and cross-file consistency

**Effort:** Medium (1–2 weeks)

---

### 3. Logging (v1.2.0)
**Goal:** Add synthetic logging analyze data with entries, severity levels, and correlation to issues.

**Details:**
- Generate log entries: synthetic logs with timestamps, severity, messages, and tags
- Include correlation IDs linking logs to traces and issues
- Support different log sources (applications, infrastructure)
- Ensure temporal consistency with other datasets

**Acceptance Criteria:**
- `logs.jsonl`: Valid log entries with realistic content
- Logs correlate with existing issues and traces where applicable
- Validation checks for temporal and referential integrity

**Effort:** Medium (1–2 weeks)

---

### 4. Synthetic Monitoring (v1.2.0)
**Goal:** Add synthetic monitoring checks and run results linked to endpoints.

**Details:**
- Generate synthetic check definitions: API and browser checks with configurations
- Create check run results: synthetic outcomes with response times, success/failure status
- Link checks to endpoints (e.g., check for "POST /checkout")
- Include alert correlations for failed checks

**Acceptance Criteria:**
- `synthetic_checks.jsonl`: Check definitions
- `synthetic_runs.jsonl`: Run results with timestamps and outcomes
- Checks reference valid endpoints
- Validation ensures realistic failure patterns

**Effort:** Medium (1–2 weeks)

---

### 5. Metric–Issue Correlation (v1.3.0)
**Goal:** Link metric spikes and anomalies directly to generated issues to increase realism and enable cause-effect testing.

**Details:**
- When generating issues, correlate them with metric spikes in `metrics_timeseries.jsonl`
- For example, if an error rate metric spikes, generate a corresponding issue with matching `entity_id` and timestamp range
- Add a `correlated_metrics` field to issues to trace which metrics triggered the issue
- Enable testing of monitoring dashboards that detect and correlate anomalies

**Acceptance Criteria:**
- Issues reference valid metric windows (e.g., latency_p95_ms spike correlates with issue start_time)
- Validation checks confirm all issue timestamps fall within metric timeframes
- Sample data demonstrates realistic cause-effect chains

**Effort:** Medium (1–2 weeks)

---

### 6. Releases & Deployments (v1.3.0)
**Goal:** Add synthetic release metadata to simulate deployment workflows.

**Details:**
- Generate release data: deployment timestamps, versions, authors, rollback info
- Link releases to applications and services
- Include deployment impact on metrics (e.g., latency changes post-deployment)

**Acceptance Criteria:**
- `releases.jsonl`: Valid release metadata
- Releases correlate with application versions and metric changes
- Validation ensures temporal consistency

**Effort:** Medium (1–2 weeks)

---

### 7. Visualization Examples (Latency/Error Charts)
**Goal:** Provide sample dashboards and charting notebooks that consume `metrics_timeseries.jsonl` to demonstrate common analyses.

**Details:**
- Create a Jupyter notebook (`examples/dashboard_examples.ipynb`) that:
  - Loads `metrics_timeseries.jsonl` and plots latency/error trends over time
  - Shows aggregated metrics per entity and per service
  - Includes scatter plots, histograms, and heatmaps of performance metrics
  - Demonstrates correlation analysis between error_rate and latency
- Create a simple HTML/Plotly dashboard template
- Provide CLI tools to generate static charts from the data
- Include instructions for integrating with Grafana or Datadog

**Acceptance Criteria:**
- Notebook runs without errors and produces 5+ visualization types
- Charts are publication-ready (labeled axes, legends, titles)
- Documentation explains how to adapt the examples for custom metrics
- Performance is acceptable (< 5s to load and plot 120 timeseries)

**Effort:** Medium (1–2 weeks)

---

## Nice-to-Have Enhancements

### 8. Advanced Scenarios
- **Cascading Failures:** Generate scenarios where one service failure triggers issues in downstream services
- **Seasonal Patterns:** Model realistic traffic patterns (peak hours, day-of-week effects)
- **Custom Distributions:** Allow users to specify custom metric distributions (e.g., Poisson for error spikes)

### 9. Integration & Export
- **Cloud Native:** Export as CloudEvents or OpenTelemetry format for compatibility with modern observability stacks
- **Database Export:** Dump to PostgreSQL/MongoDB for realistic query testing
- **API Mock:** Spin up a FastAPI/Flask mock server that serves the synthetic data as REST endpoints

### 10. Testing & Validation Enhancements
- **Schema Versioning:** Track schema versions and support backward compatibility
- **Benchmark Suite:** Compare synthetic data generation performance across versions and configurations
- **Synthetic Data Drift:** Detect and report when generated data deviates from expected distributions

---

## How to Contribute

1. Pick an enhancement from above (or propose your own in an issue)
2. Open a GitHub issue describing the work and expected outcomes
3. Link any related PRs or discussions
4. When ready, submit a PR with:
   - Implementation code
   - Updated validation checks (if applicable)
   - Documentation and sample outputs
   - Unit/integration tests

---

## Release Planning

| Version | Target | Focus |
|---------|--------|-------|
| v1.0.0  | Done   | Core synthetic datasets, validation, documentation |
| v1.1.0  | Done   | Topology graphs, alert configs, metrics catalog, entity types |
| v1.2.0  | Current | Website monitoring, mobile monitoring, logging, synthetic checks |
| v1.3.0  | Q1 2026 | Metric–issue correlation, releases, visualization examples |
| v2.0.0  | H2 2026 | Cloud-native export, full integration suite |

---

## Questions?

- Open an issue on GitHub for feature requests or discussions
- Review the `README_INSTANA.md` for current capabilities
- Check `scripts/` for code organization and patterns
