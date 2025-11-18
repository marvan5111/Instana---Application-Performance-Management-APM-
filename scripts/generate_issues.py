import json, random, time
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_issue_record, write_jsonl

def main():
    # Load entity IDs from infrastructure_entities.jsonl
    with open("data/instana/infrastructure_entities.jsonl") as f:
        blob = json.loads(next(f))
    entity_ids = [item["entity_id"] for item in blob["items"]]

    # Generate 30 issues referencing valid entity IDs
    issues = [gen_issue_record(i, entity_ids) for i in range(30)]

    write_jsonl("data/instana/issues.jsonl", issues)

if __name__ == "__main__":
    main()
