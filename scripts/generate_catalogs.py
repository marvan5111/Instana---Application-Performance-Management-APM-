import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_metrics_catalog, gen_entity_types, write_jsonl

def main():
    # Generate metrics catalog
    catalog = gen_metrics_catalog()
    write_jsonl("data/instana/metrics_catalog.jsonl", [catalog])

    # Generate entity types
    types = gen_entity_types()
    write_jsonl("data/instana/entity_types.jsonl", [types])

if __name__ == "__main__":
    main()
