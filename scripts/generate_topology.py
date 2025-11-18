import json
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_topology, write_jsonl

def main():
    # Load entity IDs from infrastructure_entities.jsonl
    with open("data/instana/infrastructure_entities.jsonl") as f:
        blob = json.loads(next(f))
    entity_ids = [item["entity_id"] for item in blob["items"]]

    # Generate infrastructure topology
    infra_topo = gen_topology(entity_ids, is_infra=True)
    write_jsonl("data/instana/infra_topology.jsonl", [infra_topo])

    # Generate application topology (using same entities for simplicity)
    app_topo = gen_topology(entity_ids, is_infra=False)
    write_jsonl("data/instana/app_topology.jsonl", [app_topo])

if __name__ == "__main__":
    main()
