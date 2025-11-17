import argparse
import json
import random
from instana_synthetic.generators import gen_issue_record, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=30)
    args = parser.parse_args()

    # Load entity_ids from infrastructure_entities.jsonl
    entity_ids = []
    try:
        with open("data/instana/infrastructure_entities.jsonl") as f:
            data = json.loads(next(f))
            entity_ids = [item["entity_id"] for item in data.get("items", [])]
    except FileNotFoundError:
        print("Warning: infrastructure_entities.jsonl not found. Using random entity_ids.")
        entity_ids = [f"srv-{15284626 + i}" for i in range(120)]

    # Generate issues with valid entity_ids
    records = []
    for i in range(args.count):
        record = gen_issue_record(i)
        record["entity_id"] = random.choice(entity_ids)  # Override with valid entity_id
        records.append(record)

    write_jsonl("data/instana/issues.jsonl", records)

if __name__ == "__main__":
    main()
