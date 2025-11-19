import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_mobile_metrics, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--minutes", type=int, default=60)
    args = parser.parse_args()
    mobile_app_ids = [f"mobile-{i+100000}" for i in range(args.count)]
    records = [gen_mobile_metrics(mid, args.minutes) for mid in mobile_app_ids]
    write_jsonl("data/instana/mobile_metrics.jsonl", records) # Corrected path

if __name__ == "__main__":
    main()
