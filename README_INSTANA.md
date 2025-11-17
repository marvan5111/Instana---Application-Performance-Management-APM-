# Instana APM Synthetic Data Generator

This branch generates synthetic data mimicking Instana Application Performance Management (APM) REST API responses. Useful for prototyping, testing, and development workflows.

## Project Completion Note

✅ **All Objectives Achieved**
- Generated synthetic datasets for 5 key Instana endpoints
- Ensured cross-file consistency (entity IDs match across datasets)
- Comprehensive validation: JSON validity, schema compliance, record counts
- All validation checks pass with no errors
- Ready for QA harness and agentic AI workflows

**Validation Summary**: All 5 datasets (120 entities, 15 apps, 40 endpoints, 120 timeseries, 30 issues) are valid JSONL with consistent entity references.

**Validation run (2025-11-17):** All validation checks executed via `validate_all.py` passed with no errors. See `validate_all.py` for reproducible validation steps and sample output.

## Scope

Synthetic datasets for key Instana endpoints:
- Infrastructure entities (`/api/infrastructure-monitoring/analyze/entities`)
- Applications (`/api/application-monitoring/applications`)
- Endpoints (`/api/application-monitoring/endpoints`)
- Metrics time series (`/api/metrics`)
- Issues/incidents (`/api/events/issues`)

Data is realistic but non-production, with plausible values, distributions, and relationships.

## Prerequisites

- Python 3.10+
- No external dependencies (uses standard library)

## Usage

### Generate All Datasets
```bash
python scripts/generate_instana_all.py --seed 42 --entities 120 --apps 15 --services 40 --issues 30
```

### Generate Specific Datasets
```bash
# Infrastructure entities
python scripts/generate_entities.py --count 200

# Metrics time series (requires entities first)
python scripts/generate_timeseries.py --minutes 120 --metric latency_p95_ms

# Applications
python scripts/generate_applications.py --count 20

# Endpoints
python scripts/generate_endpoints.py --count 50

# Issues
python scripts/generate_issues.py --count 30
```

## Outputs

Files in `data/instana/`:
- `infrastructure_entities.jsonl`: Entity health, metrics, tags
- `applications.jsonl`: App details, services, health status
- `endpoints.jsonl`: API endpoints, methods, performance metrics
- `metrics_timeseries.jsonl`: Time-series data points for entities
- `issues.jsonl`: Open/resolved issues with severity and timestamps

Each file is JSONL (one JSON object per line) for easy streaming.

## Sample Data Shapes

### Infrastructure Entity
```json
{
  "entity_health_info": {
    "max_severity": 0.82,
    "open_issues": [
      {
        "id": "ISS-521865",
        "entity_id": "srv-15284626",
        "severity": 4,
        "start": 1731799400000,
        "end": null,
        "problem_text": "Elevated latency on checkout-service"
      }
    ]
  },
  "label": "checkout-service",
  "entity_id": "srv-15284626",
  "entity_type": "Service",
  "plugin": "java",
  "snapshot_id": "snap-1050138715",
  "tags": ["env:prod", "team:payments"],
  "metrics": {
    "p95_latency_ms": 480,
    "error_rate": 0.012,
    "req_per_min": 950
  },
  "time": 1731799800000
}
```

### Metrics Time Series
```json
{
  "entity_id": "srv-15284626",
  "metric_name": "latency_p95_ms",
  "aggregation": "p95",
  "timeframe": {
    "from": 1731796200000,
    "to": 1731800000000,
    "step_ms": 60000
  },
  "points": [
    {"timestamp": 1731796200000, "value": 312},
    {"timestamp": 1731796260000, "value": 298}
  ]
}
```

## Validation

Run the comprehensive validation script to ensure data integrity:

```bash
python validate_all.py
```

### Validation Checks
- **JSON Validity**: All files parse as valid JSONL
- **Record Counts**: Confirm expected number of records per file
- **Schema Compliance**: Verify required keys and data types
- **Cross-File Consistency**: Entity IDs match between related files (e.g., issues reference valid entities)

### Sample Validation Output
```
Validating metrics_timeseries.jsonl...
metrics_timeseries.jsonl: Valid JSON, count: 120
Sample timeseries keys: ['entity_id', 'metric_name', 'aggregation', 'timeframe', 'points']
Points count: 60

Validating infrastructure_entities.jsonl...
infrastructure_entities.jsonl: Valid JSON, count: 1
Sample entity keys: ['adjusted_timeframe', 'can_load_more', 'items', 'total_hits']
Items count: 120
First item keys: ['entity_health_info', 'label', 'entity_id', 'entity_type', 'plugin', 'snapshot_id', 'tags', 'metrics', 'time']

Validating applications.jsonl...
applications.jsonl: Valid JSON, count: 15
Sample application keys: ['application_id', 'name', 'services', 'health', 'tags', 'metrics']

Validating endpoints.jsonl...
endpoints.jsonl: Valid JSON, count: 40
Sample endpoint keys: ['endpoint_id', 'path', 'method', 'service_id', 'metrics']

Validating issues.jsonl...
issues.jsonl: Valid JSON, count: 30
Sample issue keys: ['issue_id', 'entity_id', 'severity', 'state', 'start_time', 'end_time', 'problem', 'tags']

Cross-file consistency checks...
Found 120 unique entity_ids in infrastructure_entities.jsonl
All metrics timeseries entity_ids are valid.
All issues entity_ids are valid.

Validation complete.
```

## Future Work

See [`FUTURE_WORK.md`](FUTURE_WORK.md) for planned enhancements, including:

- **Metric–issue correlation:** Link metric spikes to generated issues for realistic cause-effect testing.
- **Extended endpoints:** Add alert definitions, releases, and SLO metadata.
- **Visualization examples:** Jupyter notebooks and dashboards consuming `metrics_timeseries.jsonl`.

## Notes

- Values are synthetic and randomized for realism (e.g., latency spikes, error rates).
- Entity IDs are consistent across datasets for cross-referencing.
- Use `--seed` for reproducible generation.
- Data aligns with typical Instana API responses for prototyping/QA.
- All generated data passes validation checks for integrity and consistency.
