import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_app_settings, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()

    # Load application IDs from applications.jsonl
    with open("data/instana/applications.jsonl") as f:
        app_ids = [json.loads(line)["application_id"] for line in f]

    settings = []
    for app_id in app_ids[:args.count]:  # Limit to count
        settings.append(gen_app_settings(app_id))

    write_jsonl("data/instana/app_settings.jsonl", settings)

if __name__ == "__main__":
    import random, json
    main()
