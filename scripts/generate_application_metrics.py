import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_application_metrics, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--minutes", type=int, default=60)
    args = parser.parse_args()

    # Load application IDs from applications.jsonl
    with open("data/instana/applications.jsonl") as f:
        app_ids = [json.loads(line)["application_id"] for line in f]

    metrics = []
    for app_id in app_ids[:args.count]:  # Limit to count
        # Generate multiple metrics per application
        for metric in ["latency_p95_ms", "throughput_rpm", "apdex_score", "error_rate_percent"]:
            metrics.append(gen_application_metrics(app_id, metric, args.minutes))

    write_jsonl("data/instana/application_metrics.jsonl", metrics)

if __name__ == "__main__":
    import random, json
    main()
