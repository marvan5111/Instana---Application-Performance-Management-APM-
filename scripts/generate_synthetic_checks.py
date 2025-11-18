import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_synthetic_check, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    args = parser.parse_args()
    endpoint_ids = [f"ep-{i+100000}" for i in range(10)]  # sample endpoint_ids
    records = [gen_synthetic_check(endpoint_ids) for _ in range(args.count)]
    write_jsonl("data/instana/synthetic_checks.jsonl", records)

if __name__ == "__main__":
    main()
