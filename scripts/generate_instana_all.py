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

    print("All Instana synthetic data generated successfully!")

if __name__ == "__main__":
    main()
