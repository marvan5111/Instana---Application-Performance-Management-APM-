import argparse
from instana_synthetic.generators import gen_application, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    args = parser.parse_args()
    records = [gen_application(i) for i in range(args.count)]
    write_jsonl("data/instana/applications.jsonl", records)

if __name__ == "__main__":
    main()
