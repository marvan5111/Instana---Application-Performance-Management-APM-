 # Release Notes: v1.1.0 - Topology, Alerts, and Catalogs
 
 ## Overview
 
 Version 1.1.0 builds upon the core data generation framework established in v1.0.0 by introducing critical metadata and relationship datasets. This release significantly enhances the realism of the synthetic environment by adding infrastructure and application topology graphs, alert configurations, and metadata catalogs for metrics and entity types.
 
 These additions are essential for testing more advanced APM features, such as dependency mapping, alert configuration management, and automated monitoring setup.
 
 ## ✅ Key Features Delivered
 
 This release expands the synthetic data suite with 5 new datasets, all validated for structural and relational integrity.
 
 1.  **Infrastructure Topology** (`infra_topology.jsonl`)
     -   Generates a graph structure of nodes and edges, representing the relationships between infrastructure entities (e.g., hosts connected to services).
 
 2.  **Application Topology** (`app_topology.jsonl`)
     -   Provides a high-level dependency map for applications, showing how different applications and services interact.
 
 3.  **Alert Configurations** (`alert_configs.jsonl`)
     -   Creates a set of synthetic alert rules, including metric thresholds (e.g., `latency > 500ms`), severity levels, and notification channels. These configurations are linked to valid entities.
 
 4.  **Metrics Catalog** (`metrics_catalog.jsonl`)
     -   Defines a catalog of available metrics, including their names, units, and aggregation types (e.g., `p95`, `avg`).
 
 5.  **Entity Types Catalog** (`entity_types.jsonl`)
     -   Provides a catalog of monitorable entity types (e.g., `Service`, `Host`, `Container`), which is fundamental for dynamic monitoring tools.
 
 ## ⚙️ Code Summary
 
 To support these new datasets, the following enhancements were made to the codebase:
 
 -   **`instana_synthetic/generators.py`**: New generator functions were added:
     -   `gen_topology()`: Creates graph structures with nodes and edges, ensuring that node IDs are consistent with the main entity list.
     -   `gen_alert_config()`: Produces realistic alert rules linked to valid entity IDs.
     -   `gen_metrics_catalog()` and `gen_entity_types()`: Generate static but essential metadata catalogs.
 -   **`scripts/`**: New orchestration scripts were added to generate the topology, alerts, and catalog files (`generate_topology.py`, `generate_alert_configs.py`, `generate_catalogs.py`).
 -   **`scripts/generate_instana_all.py`**: The main generation script was updated to include these new scripts in its workflow.
 -   **`validate_all.py`**: The validation suite was significantly upgraded to include:
     -   **Topology Validation**: Checks that all node IDs in `infra_topology.jsonl` correspond to existing entities.
     -   **Alert Config Validation**: Verifies that all `entity_id`s in `alert_configs.jsonl` are valid.
 
 ## 🧪 Validation Output
 
 The following is the expected output from running `python validate_all.py` against the datasets included in the v1.1.0 release.
 
 ```
 Validating infra_topology.jsonl...
 infra_topology.jsonl: Valid JSON, count: 1
 Sample topology keys: ['nodes', 'edges']
 Nodes count: 20
 Edges count: 19
 
 Validating app_topology.jsonl...
 app_topology.jsonl: Valid JSON, count: 1
 
 Validating alert_configs.jsonl...
 alert_configs.jsonl: Valid JSON, count: 25
 Sample alert keys: ['alert_id', 'name', 'entity_id', 'rule', 'severity', 'enabled', 'notification_channels']
 
 Validating metrics_catalog.jsonl...
 metrics_catalog.jsonl: Valid JSON, count: 1
 Sample catalog keys: ['metrics']
 Metrics count: 5
 
 Validating entity_types.jsonl...
 entity_types.jsonl: Valid JSON, count: 1
 Sample types keys: ['entity_types']
 Types count: 5
 
 Cross-file consistency for topology...
 All topology node IDs are valid.
 
 Cross-file consistency for alerts...
 All alert config entity_ids are valid.
 
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
 
 -   `instana-synthetic-v1.1.0.zip`: A zip archive containing all 10 generated datasets (5 from v1.0.0 + 5 new).
 -   `validation_log_v1.1.0.txt`: The full output log from the validation script.