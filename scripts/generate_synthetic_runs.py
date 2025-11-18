import argparse
import random
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_synthetic_run, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100)
    args = parser.parse_args()
    # Read check_ids from the generated synthetic_checks.jsonl
    check_ids = []
    try:
        with open("data/instana/synthetic_checks.jsonl", "r") as f:
            for line in f:
                import json
                data = json.loads(line)
                check_ids.append(data['check_id'])
    except FileNotFoundError:
        check_ids = [f"chk-{random.randint(100000,999999)}" for _ in range(20)]  # fallback
    records = [gen_synthetic_run(random.choice(check_ids)) for _ in range(args.count)]
    write_jsonl("data/instana/synthetic_runs.jsonl", records)

if __name__ == "__main__":
    main()
