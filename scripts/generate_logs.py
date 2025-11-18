import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_log_entry, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100)
    args = parser.parse_args()
    entity_ids = [f"srv-{15284626 + i}" for i in range(10)]  # sample entity_ids
    records = [gen_log_entry(entity_ids) for _ in range(args.count)]
    write_jsonl("data/instana/logs.jsonl", records)

if __name__ == "__main__":
    main()
