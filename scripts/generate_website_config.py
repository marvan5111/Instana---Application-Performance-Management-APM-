import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_website_config, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()
    records = [gen_website_config(i) for i in range(args.count)]
    write_jsonl("data/instana/website_config.jsonl", records)

if __name__ == "__main__":
    main()
