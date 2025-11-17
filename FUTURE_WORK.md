# Future Work Roadmap

This document outlines planned enhancements and improvements for the Instana APM Synthetic Data Generator beyond v1.0.0.

## Priority Enhancements

### 1. Metric–Issue Correlation (Realism)
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

### 2. Extended Endpoints (Alerts, Releases)
**Goal:** Add synthetic alerting and release metadata to endpoints and applications to simulate full delivery/ops workflows.

**Details:**
- Generate alert definitions (thresholds, notification channels, on-call assignments)
- Add release metadata: deployment timestamps, versions, rollback info, change authors
- Link alerts to endpoints (e.g., "POST /checkout alerts if error_rate > 5%")
- Include health check / SLO definitions per endpoint
- Support multi-region / multi-environment deployment scenarios

**Acceptance Criteria:**
- Endpoints include `alerts` field with threshold and notification config
- Applications include `recent_releases` with deployment timestamps and versions
- Validation checks ensure alert thresholds make sense (e.g., error_rate 0–100%)
- Sample data shows realistic alert–release–metric correlations

**Effort:** Large (2–3 weeks)

---

### 3. Visualization Examples (Latency/Error Charts)
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

### 4. Advanced Scenarios
- **Cascading Failures:** Generate scenarios where one service failure triggers issues in downstream services
- **Seasonal Patterns:** Model realistic traffic patterns (peak hours, day-of-week effects)
- **Custom Distributions:** Allow users to specify custom metric distributions (e.g., Poisson for error spikes)

### 5. Integration & Export
- **Cloud Native:** Export as CloudEvents or OpenTelemetry format for compatibility with modern observability stacks
- **Database Export:** Dump to PostgreSQL/MongoDB for realistic query testing
- **API Mock:** Spin up a FastAPI/Flask mock server that serves the synthetic data as REST endpoints

### 6. Testing & Validation Enhancements
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
| v1.1.0  | Q4 2025 | Metric–issue correlation, visualization examples |
| v1.2.0  | Q1 2026 | Extended endpoints (alerts, releases), advanced scenarios |
| v2.0.0  | H2 2026 | Cloud-native export, full integration suite |

---

## Questions?

- Open an issue on GitHub for feature requests or discussions
- Review the `README_INSTANA.md` for current capabilities
- Check `scripts/` for code organization and patterns
