import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_website_catalog, write_jsonl

def main():
    record = gen_website_catalog()
    write_jsonl("data/instana/website_catalog.jsonl", [record])

if __name__ == "__main__":
    main()
