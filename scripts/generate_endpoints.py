import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_endpoint, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=50)
    args = parser.parse_args()
    records = [gen_endpoint(i) for i in range(args.count)]
    write_jsonl("data/instana/endpoints.jsonl", records)

if __name__ == "__main__":
    main()
