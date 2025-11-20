 # TODO: v1.6.0 – Cloud Native Integration
 
 ## Overview
 Integrate the APM platform with the cloud-native ecosystem by adding support for Kubernetes metrics, Prometheus/Grafana exports, and real-time streaming analytics.
 
 ## 1. Kubernetes Metrics Generators
 - [ ] Create `gen_kubernetes_pod()` in `generators.py` for Pods (CPU, memory, restarts, status).
 - [ ] Create `gen_kubernetes_cluster()` in `generators.py` for Clusters (node count, health).
 - [ ] Create `gen_kubernetes_deployment()` in `generators.py` for Deployments (replicas, rollout status).
 - [ ] Create `scripts/generate_kubernetes_pods.py`.
 - [ ] Create `scripts/generate_kubernetes_clusters.py`.
 - [ ] Create `scripts/generate_kubernetes_deployments.py`.
 - [ ] Update `generate_instana_all.py` to include new Kubernetes scripts.
 - [ ] Add validation for new Kubernetes files in `validate_all.py`.
 
 ## 2. Prometheus/Grafana Export
 - [ ] Enhance `prometheus_exporter.py` to handle all metric types.
 - [ ] Create a sample `prometheus.yml` for scraping exported metrics.
 - [ ] Create sample Grafana dashboard JSON templates.
 - [ ] Add export options to `run_data_generation.sh`.
 
 ## 3. Streaming Analytics (Kafka/Flink)
 - [ ] Implement a Kafka producer to stream events (`streaming_connectors.py`).
 - [ ] Create a sample Flink/Spark job for real-time anomaly detection on the stream.
 - [ ] Test pipeline with 100k+ events/hour.
 
 ## 4. Multi-Region Simulation
 - [ ] Extend generators to add `region` (APAC, EMEA, AMER) attributes.
 - [ ] Simulate regional latency variations and error rates.
 - [ ] Add a "Cloud Native" tab to `dashboard.py` with region filters and Kubernetes visualizations.
 
 ## 📊 Acceptance Criteria
 - [ ] Kubernetes metrics are generated and validated.
 - [ ] Prometheus can successfully scrape the exported metrics file.
 - [ ] Grafana dashboard imports and displays data.
 - [ ] Kafka streaming pipeline is stable under load.
 - [ ] Regional data is correctly simulated and visualized.