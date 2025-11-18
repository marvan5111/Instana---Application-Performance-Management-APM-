import json
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_alert_config, write_jsonl

def main():
    # Load entity IDs from infrastructure_entities.jsonl
    with open("data/instana/infrastructure_entities.jsonl") as f:
        blob = json.loads(next(f))
    entity_ids = [item["entity_id"] for item in blob["items"]]

    # Generate alert configs: 10 app, 10 infra, 5 synthetic
    alerts = []
    for _ in range(10):
        alerts.append(gen_alert_config(entity_ids, "app"))
    for _ in range(10):
        alerts.append(gen_alert_config(entity_ids, "infra"))
    for _ in range(5):
        alerts.append(gen_alert_config(entity_ids, "synthetic"))

    write_jsonl("data/instana/alert_configs.jsonl", alerts)

if __name__ == "__main__":
    main()
