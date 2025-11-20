import json
import os

def validate_metrics(metrics_file, dashboard_file):
    """
    Validates that the generated metrics contain the expressions
    and labels required by the Grafana dashboard.
    """
    print(f"Validating {metrics_file} against {dashboard_file}...")

    if not os.path.exists(metrics_file):
        print(f"Error: Metrics file not found at {metrics_file}")
        return False

    with open(dashboard_file, 'r') as f:
        dashboard = json.load(f)

    with open(metrics_file, 'r') as f:
        metrics_data = json.load(f)

    required_metrics = {panel['targets'][0]['expr'] for panel in dashboard['dashboard']['panels']}
    found_metrics = {metric['metric'] for metric in metrics_data}

    missing_metrics = required_metrics - found_metrics
    if missing_metrics:
        print(f"Validation Failed: The following metrics required by the dashboard are missing from the generated data:")
        for metric in missing_metrics:
            print(f" - {metric}")
        return False

    print("Validation Successful: All required metrics are present in the generated data.")
    # A full implementation would also check for labels like 'cluster_id', 'region', etc.
    # This is a good starting point.
    return True

def main():
    metrics_file = 'data/instana/kubernetes_metrics.jsonl'
    dashboard_file = 'grafana_dashboards/kubernetes_metrics.json'
    
    if not validate_metrics(metrics_file, dashboard_file):
        # Exit with a non-zero status code to indicate failure
        exit(1)

if __name__ == "__main__":
    main()