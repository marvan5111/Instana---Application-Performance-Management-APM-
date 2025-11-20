import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_api_tokens, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    tokens = []
    for i in range(args.count):
        tokens.append(gen_api_tokens())

    write_jsonl("data/instana/api_tokens.jsonl", tokens)

if __name__ == "__main__":
    main()
