import argparse
from instana_synthetic.generators import rand_timeframe, gen_entity, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=100)
    args = parser.parse_args()
    records = {
        "adjusted_timeframe": rand_timeframe(minutes=15),
        "can_load_more": False,
        "items": [gen_entity(i) for i in range(args.count)],
        "total_hits": args.count
    }
    write_jsonl("data/instana/infrastructure_entities.jsonl", [records])

if __name__ == "__main__":
    main()
