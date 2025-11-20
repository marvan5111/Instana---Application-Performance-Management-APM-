# Instana APM Synthetic Data Generator

This repository provides an end-to-end operational intelligence platform, featuring a synthetic data generator that mimics Instana APM responses, a real-time monitoring dashboard, and a proactive alerting system. It is a portfolio-grade project demonstrating full-stack Python development.

## ✨ Highlights

🎯 **v1.3.0: Full Operational Intelligence Platform**
- **Interactive Dashboard**: A real-time monitoring dashboard built with Plotly Dash, visualizing metrics for websites, mobile apps, synthetic checks, and logs.
- **Proactive Alerting**: A configurable alerting system that sends notifications via Slack and email for performance degradation or failures.
- **Advanced Synthetic Monitoring**: Simulates multi-step user journeys (e.g., login → search → checkout) to validate critical application flows.
- **Comprehensive Data Generation**: Generates 16+ validated datasets covering infrastructure, applications, mobile, synthetics, and logging.
- **Secure & Deployable**: Includes basic authentication and is configured for production deployment on platforms like Heroku, AWS, or Azure.

## Quick Start

### 🐳 Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/instana-apm-dashboard.git
cd instana-apm-dashboard

# Run with Docker Compose
docker-compose up -d

# Access dashboard at http://localhost:8050
# Default credentials: admin / instana
```

### 🐍 Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python scripts/generate_instana_all.py --seed 42 --entities 120 --apps 15 --services 40 --issues 30
python validate_all.py

# Run dashboard
python dashboard.py

# Access at http://127.0.0.1:8050
```

### ☁️ Cloud Deployment
```bash
# Heroku (one-click)
heroku create your-app-name
git push heroku main

# AWS/Azure - see DEPLOYMENT_GUIDE.md
```

## Enterprise Features

### 🔐 Multi-Tenant Architecture
- **Tenant Isolation**: Data segregation by tenant ID with secure access controls
- **RBAC**: Admin, Editor, Viewer, Operator roles with granular permissions
- **SSO Integration**: OAuth2, LDAP/Active Directory support
- **Audit Logging**: Complete audit trail of user actions and system events

### 📊 Dashboard Screenshots

#### Overview Dashboard
![Overview Dashboard](screenshots/overview-dashboard.png)
*Real-time KPIs, system health gauges, and cross-platform performance comparison*

#### Multi-Tenant Monitoring
![Multi-Tenant Dashboard](screenshots/multi-tenant-dashboard.png)
*Tenant-aware data visualization with role-based access controls*

#### Anomaly Detection
![Anomaly Detection](screenshots/anomaly-detection.png)
*Statistical anomaly detection with confidence intervals and alert correlation*

### 🚀 Usage Examples

```python
from dashboard import app
from audit_logger import audit_logger

# Initialize with tenant context
app.config['TENANT_ID'] = 'tenant-1'

# Log user action
audit_logger.log_action(
    user_id='admin_user',
    action='dashboard_access',
    resource_type='dashboard',
    resource_id='overview',
    details={'tab': 'overview'},
    tenant_id='tenant-1'
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
```

**Generate tenant-specific data:**
```bash
# Generate data for specific tenant
python scripts/generate_instana_all.py --tenant-id tenant-1 --seed 42 --entities 120

# Validate with tenant isolation
python validate_all.py --tenant tenant-1
```

## Project Completion Note

✅ **All Objectives Achieved**
- Generated synthetic datasets for 10 key Instana endpoints
- Ensured cross-file consistency (entity IDs match across datasets)
- Comprehensive validation: JSON validity, schema compliance, record counts
- All validation checks pass with no errors
- Ready for QA harness and agentic AI workflows

**Validation Summary**: All 10 datasets (120 entities, 15 apps, 40 endpoints, 120 timeseries, 30 issues, topology graphs, alert configs, catalogs) are valid JSONL with consistent entity references.

**Validation run (2025-11-17):** All validation checks executed via `validate_all.py` passed with no errors. See `validate_all.py` for reproducible validation steps and sample output.

## Scope

Synthetic datasets for key Instana endpoints:
- Infrastructure entities (`/api/infrastructure-monitoring/analyze/entities`)
- Applications (`/api/application-monitoring/applications`)
- Endpoints (`/api/application-monitoring/endpoints`)
- Metrics time series (`/api/metrics`)
- Issues/incidents (`/api/events/issues`)
- Infrastructure topology (`/api/infrastructure-monitoring/topology`)
- Application topology (`/api/application-monitoring/topology`)
- Alert configurations (`/api/settings/alerting/configurations`)
- Metrics catalog (`/api/catalog/metrics`)
- Entity types (`/api/catalog/entity-types`)

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
- `infra_topology.jsonl`: Infrastructure topology graphs with nodes and edges
- `app_topology.jsonl`: Application topology graphs with nodes and edges
- `alert_configs.jsonl`: Alert configuration rules and thresholds
- `metrics_catalog.jsonl`: Catalog of available metrics with metadata
- `entity_types.jsonl`: Catalog of available entity types

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

### Validation Results (v1.1.0)

✅ **All validation checks passed** with zero errors.

**Dataset Summary:**
| Dataset | File | Records | Status |
|---------|------|---------|--------|
| Infrastructure Entities | `infrastructure_entities.jsonl` | 120 items | ✅ Valid |
| Applications | `applications.jsonl` | 15 apps | ✅ Valid |
| Endpoints | `endpoints.jsonl` | 40 endpoints | ✅ Valid |
| Metrics Time Series | `metrics_timeseries.jsonl` | 120 series (60 points each) | ✅ Valid |
| Issues/Incidents | `issues.jsonl` | 30 issues | ✅ Valid |
| Infra Topology | `infra_topology.jsonl` | 1 graph (20 nodes, 19 edges) | ✅ Valid |
| App Topology | `app_topology.jsonl` | 1 graph | ✅ Valid |
| Alert Configs | `alert_configs.jsonl` | 25 configs | ✅ Valid |
| Metrics Catalog | `metrics_catalog.jsonl` | 1 catalog (5 metrics) | ✅ Valid |
| Entity Types | `entity_types.jsonl` | 1 catalog (5 types) | ✅ Valid |

**Cross-File Consistency:**
- ✅ Found 120 unique `entity_ids` in `infrastructure_entities.jsonl`
- ✅ All metrics timeseries `entity_ids` reference valid entities
- ✅ All issues `entity_ids` reference valid entities
- ✅ No orphaned references or data integrity issues

**Full Validation Log:**
Download the complete validation log from the [v1.1.0-instana-synthetic Release](https://github.com/marvan5111/Instana---Application-Performance-Management-APM-/releases/tag/v1.1.0-instana-synthetic) (attached as `validation_log.txt`).

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
