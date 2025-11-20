from typing import List, Dict
import json
import os

def to_prometheus_format(metric_name: str, labels: Dict, value: float, timestamp_ms: int = None) -> str:
    """
    Convert a single metric to Prometheus text exposition format.
    Example: http_requests_total{method="post",code="200"} 1027 1395066363000
    """
    label_str = ",".join([f'{key}="{value}"' for key, value in labels.items()])
    metric_str = f"{metric_name}{{{label_str}}} {value}"
    if timestamp_ms:
        metric_str += f" {timestamp_ms}"
    return metric_str

def export_metrics_to_prometheus(timeseries_data: List[Dict], output_file: str):
    """
    Export timeseries data to a file in Prometheus exposition format.
    """
    prom_lines = []
    for record in timeseries_data:
        metric_name = record.get("metric_name", "unknown_metric")
        entity_id = record.get("entity_id", "unknown_entity")

        for point in record.get("points", []):
            labels = {"entity_id": entity_id}
            prom_line = to_prometheus_format(metric_name, labels, point['value'], point['timestamp'])
            prom_lines.append(prom_line)

    try:
        with open(output_file, 'w') as f:
            f.write("\n".join(prom_lines))
        print(f"Successfully exported {len(prom_lines)} metric points to {output_file}")
    except Exception as e:
        print(f"Error exporting to Prometheus format: {e}")

def export_all_metrics_to_prometheus(output_file: str):
    """
    Export all available metrics (application, infrastructure, Kubernetes) to Prometheus format.
    """
    prom_lines = []

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Export application metrics
    if os.path.exists('data/instana/application_metrics.jsonl'):
        with open('data/instana/application_metrics.jsonl', 'r') as f:
            for line in f:
                record = json.loads(line)
                metric_name = record.get("metric_name", "unknown_metric")
                app_id = record.get("application_id", "unknown_app")

                for point in record.get("points", []):
                    labels = {"application_id": app_id, "type": "application"}
                    prom_line = to_prometheus_format(metric_name, labels, point['value'], point['timestamp'])
                    prom_lines.append(prom_line)

    # Export infrastructure metrics
    if os.path.exists('data/instana/infrastructure_metrics.jsonl'):
        with open('data/instana/infrastructure_metrics.jsonl', 'r') as f:
            for line in f:
                record = json.loads(line)
                metric_name = record.get("metric_name", "unknown_metric")
                entity_id = record.get("entity_id", "unknown_entity")

                for point in record.get("points", []):
                    labels = {"entity_id": entity_id, "type": "infrastructure"}
                    prom_line = to_prometheus_format(metric_name, labels, point['value'], point['timestamp'])
                    prom_lines.append(prom_line)

    # Export Kubernetes metrics
    if os.path.exists('data/instana/kubernetes_pods.jsonl'):
        with open('data/instana/kubernetes_pods.jsonl', 'r') as f:
            for line in f:
                record = json.loads(line)
                pod_id = record.get("pod_id", "unknown_pod")
                cluster_id = record.get("cluster_id", "unknown_cluster")
                deployment_id = record.get("deployment_id", "unknown_deployment")
                namespace = record.get("namespace", "default")
                status = record.get("status", "unknown")

                # CPU usage
                cpu_cores = record.get("metrics", {}).get("cpu_usage_cores", 0)
                labels = {"pod_id": pod_id, "cluster_id": cluster_id, "deployment_id": deployment_id,
                         "namespace": namespace, "status": status, "type": "kubernetes"}
                prom_line = to_prometheus_format("kubernetes_pod_cpu_usage_cores", labels, cpu_cores, record.get("time"))
                prom_lines.append(prom_line)

                # Memory usage
                memory_mb = record.get("metrics", {}).get("memory_usage_mb", 0)
                prom_line = to_prometheus_format("kubernetes_pod_memory_usage_mb", labels, memory_mb, record.get("time"))
                prom_lines.append(prom_line)

    # Export cluster metrics
    if os.path.exists('data/instana/kubernetes_clusters.jsonl'):
        with open('data/instana/kubernetes_clusters.jsonl', 'r') as f:
            for line in f:
                record = json.loads(line)
                cluster_id = record.get("cluster_id", "unknown_cluster")
                region = record.get("region", "unknown_region")
                status = record.get("status", "unknown")

                labels = {"cluster_id": cluster_id, "region": region, "status": status, "type": "kubernetes"}

                # Node count
                node_count = record.get("metrics", {}).get("total_cpu_cores", 0) // 8  # Approximate nodes
                prom_line = to_prometheus_format("kubernetes_cluster_node_count", labels, node_count, record.get("time"))
                prom_lines.append(prom_line)

                # CPU utilization
                cpu_util = record.get("metrics", {}).get("cpu_utilization_percent", 0)
                prom_line = to_prometheus_format("kubernetes_cluster_cpu_utilization_percent", labels, cpu_util, record.get("time"))
                prom_lines.append(prom_line)

                # Memory utilization
                mem_util = record.get("metrics", {}).get("memory_utilization_percent", 0)
                prom_line = to_prometheus_format("kubernetes_cluster_memory_utilization_percent", labels, mem_util, record.get("time"))
                prom_lines.append(prom_line)

    try:
        with open(output_file, 'w') as f:
            f.write("\n".join(prom_lines))
        print(f"Successfully exported {len(prom_lines)} metric points to {output_file}")
    except Exception as e:
        print(f"Error exporting to Prometheus format: {e}")

if __name__ == "__main__":
    # Example Usage
    from instana_synthetic.generators import gen_timeseries
    ts_data = [gen_timeseries(f"srv-{i}") for i in range(3)]
    export_metrics_to_prometheus(ts_data, "data/exports/metrics.prom")

    # Export all metrics
    export_all_metrics_to_prometheus("data/exports/all_metrics.prom")
