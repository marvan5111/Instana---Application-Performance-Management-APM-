import argparse
import subprocess
import sys

def run_script(script, args):
    cmd = [sys.executable, script] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {script}: {result.stderr}")
        sys.exit(1)
    else:
        print(f"Successfully ran {script}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--entities", type=int, default=120)
    parser.add_argument("--apps", type=int, default=15)
    parser.add_argument("--services", type=int, default=40)
    parser.add_argument("--issues", type=int, default=30)
    args = parser.parse_args()

    import random
    random.seed(args.seed)

    # Generate entities
    run_script("scripts/generate_entities.py", ["--count", str(args.entities)])

    # Generate applications
    run_script("scripts/generate_applications.py", ["--count", str(args.apps)])

    # Generate endpoints
    run_script("scripts/generate_endpoints.py", ["--count", str(args.services)])

    # Generate issues
    run_script("scripts/generate_issues.py", ["--count", str(args.issues)])

    # Generate timeseries (depends on entities)
    run_script("scripts/generate_timeseries.py", ["--minutes", "60"])

    # Generate topology
    run_script("scripts/generate_topology.py", [])

    # Generate alert configs
    run_script("scripts/generate_alert_configs.py", [])

    # Generate catalogs
    run_script("scripts/generate_catalogs.py", [])

    # Generate website monitoring
    run_script("scripts/generate_website_config.py", ["--count", "10"])
    run_script("scripts/generate_website_catalog.py", [])
    run_script("scripts/generate_website_metrics.py", ["--count", "10", "--minutes", "60"])
    run_script("scripts/generate_website_analyze.py", ["--count", "10"])

    # Generate logging
    run_script("scripts/generate_logs.py", ["--count", "100"])

    # Generate synthetic checks
    run_script("scripts/generate_synthetic_checks.py", ["--count", "20"])
    run_script("scripts/generate_synthetic_runs.py", ["--count", "100"])

    # Generate mobile monitoring
    run_script("scripts/generate_mobile_config.py", ["--count", "10"])
    run_script("scripts/generate_mobile_catalog.py", [])
    run_script("scripts/generate_mobile_metrics.py", ["--count", "10", "--minutes", "60"])
    run_script("scripts/generate_mobile_analyze.py", ["--count", "10"])

    # Generate v1.4.0 infrastructure monitoring
    run_script("scripts/generate_infrastructure_entities.py", ["--count", "50"])
    run_script("scripts/generate_infrastructure_metrics.py", ["--count", "20", "--minutes", "60"])
    run_script("scripts/generate_infra_topology.py", ["--count", "5"])

    # Generate v1.4.0 application enhancements
    run_script("scripts/generate_application_metrics.py", ["--count", "20", "--minutes", "60"])
    run_script("scripts/generate_application_traces.py", ["--count", "10"])
    run_script("scripts/generate_app_topology.py", ["--count", "5"])
    run_script("scripts/generate_app_settings.py", ["--count", "10"])

    # Generate v1.4.0 alert configurations
    run_script("scripts/generate_global_alert_configs.py", ["--count", "10"])
    run_script("scripts/generate_infra_alert_configs.py", ["--count", "10"])

    # Generate v1.4.0 event settings and host agent
    run_script("scripts/generate_event_settings.py", ["--count", "5"])
    run_script("scripts/generate_host_agent_status.py", ["--count", "20"])
    run_script("scripts/generate_events.py", ["--count", "50"])

    # Generate v1.4.0 user management
    run_script("scripts/generate_user_roles.py", [])
    run_script("scripts/generate_api_tokens.py", ["--count", "5"])
    run_script("scripts/generate_access_catalogs.py", [])

    # Generate v1.6.0 Kubernetes monitoring
    run_script("scripts/generate_kubernetes_data.py", ["--clusters", "10", "--deployments-per-cluster", "5", "--pods-per-deployment", "3"])

    # Validate Kubernetes data for dashboard
    run_script("scripts/validate_kubernetes.py", [])

    print("All Instana synthetic data generated successfully!")

if __name__ == "__main__":
    main()
