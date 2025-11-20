import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_application_traces, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()

    # Load application IDs from applications.jsonl
    with open("data/instana/applications.jsonl") as f:
        app_ids = [json.loads(line)["application_id"] for line in f]

    traces = []
    for app_id in app_ids[:args.count]:  # Limit to count
        traces.append(gen_application_traces(app_id, span_count=5))

    write_jsonl("data/instana/application_traces.jsonl", traces)

if __name__ == "__main__":
    import random, json
    main()
