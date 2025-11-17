import argparse, random
from instana_synthetic.generators import gen_timeseries, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entities-file", default="data/instana/infrastructure_entities.jsonl")
    parser.add_argument("--metric", default="latency_p95_ms")
    parser.add_argument("--minutes", type=int, default=60)
    parser.add_argument("--out", default="data/instana/metrics_timeseries.jsonl")
    args = parser.parse_args()

    with open(args.entities_file) as f:
        blob = json.loads(next(f))
    entity_ids = [item["entity_id"] for item in blob["items"]]

    records = [gen_timeseries(eid, args.metric, args.minutes) for eid in entity_ids]
    write_jsonl(args.out, records)

if __name__ == "__main__":
    import json
    main()
