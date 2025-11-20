import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_access_catalogs, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    catalogs = gen_access_catalogs()
    write_jsonl("data/instana/access_catalogs.jsonl", catalogs["access_catalogs"])

if __name__ == "__main__":
    main()
