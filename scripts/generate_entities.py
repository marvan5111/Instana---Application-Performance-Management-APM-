import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import rand_timeframe, gen_infrastructure_entity, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=120)
    args = parser.parse_args()

    entities = []
    # Generate mix of hosts, containers, and processes
    for i in range(args.count):
        entity_type = random.choice(["host", "container", "process"])
        entities.append(gen_infrastructure_entity(entity_type))

    records = {
        "adjusted_timeframe": rand_timeframe(minutes=15),
        "can_load_more": False,
        "items": entities,
        "total_hits": len(entities)
    }
    write_jsonl("data/instana/infrastructure_entities.jsonl", [records])

if __name__ == "__main__":
    from instana_synthetic.generators import now_ms
    import random
    main()
