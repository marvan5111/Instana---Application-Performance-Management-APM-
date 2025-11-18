import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_website_metrics, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--minutes", type=int, default=60)
    args = parser.parse_args()
    website_ids = [f"web-{i+100000}" for i in range(args.count)]
    records = [gen_website_metrics(wid, args.minutes) for wid in website_ids]
    write_jsonl("data/instana/website_metrics.jsonl", records)

if __name__ == "__main__":
    main()
