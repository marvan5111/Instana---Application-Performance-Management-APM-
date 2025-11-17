# Instana APM Synthetic Data Generator

This branch generates synthetic data mimicking Instana Application Performance Management (APM) REST API responses. Useful for prototyping, testing, and development workflows.

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

## Notes

- Values are synthetic and randomized for realism (e.g., latency spikes, error rates).
- Entity IDs are consistent across datasets for cross-referencing.
- Use `--seed` for reproducible generation.
- Data aligns with typical Instana API responses for prototyping/QA.
