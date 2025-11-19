import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_mobile_catalog, write_jsonl

def main():
    record = gen_mobile_catalog()
    write_jsonl("data/instana/mobile_catalog.jsonl", [record]) # Corrected path

if __name__ == "__main__":
    main()
