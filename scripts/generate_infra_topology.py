import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_infra_topology, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    # Load entity IDs from infrastructure_entities.jsonl
    with open("data/instana/infrastructure_entities.jsonl") as f:
        blob = json.loads(next(f))
    entity_ids = [item["entity_id"] for item in blob["items"]]

    topologies = []
    for i in range(args.count):
        topologies.append(gen_infra_topology(entity_ids))

    write_jsonl("data/instana/infra_topology.jsonl", topologies)

if __name__ == "__main__":
    import json
    main()
