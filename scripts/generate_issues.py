import json, random, time

def now_ms():
    return int(time.time() * 1000)

def gen_issue(entity_ids):
    eid = random.choice(entity_ids)
    return {
        "issue_id": f"ISS-{random.randint(100000,999999)}",
        "entity_id": eid,
        "severity": random.randint(1,5),
        "state": random.choice(["open","closed"]),
        "start_time": now_ms() - random.randint(1,30)*60_000,
        "end_time": None if random.random() < 0.7 else now_ms(),
        "problem": random.choice([
            "Elevated latency",
            "Error rate spike",
            "CPU saturation"
        ]),
        "tags": random.sample(
            ["env:prod","team:payments","region:us","region:apac","team:core"], k=2
        )
    }

def main():
    # Load entity IDs from infrastructure_entities.jsonl
    with open("data/instana/infrastructure_entities.jsonl") as f:
        blob = json.loads(next(f))
    entity_ids = [item["entity_id"] for item in blob["items"]]

    # Generate 30 issues referencing valid entity IDs
    issues = [gen_issue(entity_ids) for _ in range(30)]

    with open("data/instana/issues.jsonl", "w") as out:
        for issue in issues:
            out.write(json.dumps(issue) + "\n")

if __name__ == "__main__":
    main()
