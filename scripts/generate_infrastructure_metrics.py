import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_infrastructure_metrics, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--minutes", type=int, default=60)
    args = parser.parse_args()

    # Load entity IDs from infrastructure_entities.jsonl
    with open("data/instana/infrastructure_entities.jsonl") as f:
        blob = json.loads(next(f))
    entity_ids = [item["entity_id"] for item in blob["items"]]

    metrics = []
    for entity_id in entity_ids[:args.count]:  # Limit to count
        entity_type = entity_id.split('-')[0]
        # Generate multiple metrics per entity
        for metric in ["cpu_usage_percent", "memory_usage_percent", "network_rx_mbps", "network_tx_mbps"]:
            if entity_type == "host" or (entity_type == "container" and metric in ["cpu_usage_percent", "memory_usage_percent", "network_rx_mbps", "network_tx_mbps"]) or (entity_type == "process" and metric in ["cpu_percent", "memory_mb"]):
                metrics.append(gen_infrastructure_metrics(entity_id, metric, args.minutes))

    write_jsonl("data/instana/infrastructure_metrics.jsonl", metrics)

if __name__ == "__main__":
    import random, json
    main()
