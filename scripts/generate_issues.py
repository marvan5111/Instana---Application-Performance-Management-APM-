import argparse
from instana_synthetic.generators import gen_issue_record, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=30)
    args = parser.parse_args()
    records = [gen_issue_record(i) for i in range(args.count)]
    write_jsonl("data/instana/issues.jsonl", records)

if __name__ == "__main__":
    main()
