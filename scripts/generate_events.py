import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_events, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=50)
    args = parser.parse_args()

    # Generate entity IDs for correlation
    entity_ids = [f"entity-{random.randint(100000,999999)}" for _ in range(20)]
    events = gen_events(entity_ids, args.count)

    write_jsonl("data/instana/events.jsonl", events)

if __name__ == "__main__":
    import random
    main()
