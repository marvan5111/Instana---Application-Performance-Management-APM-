import json

# Validate metrics_timeseries.jsonl
print("Validating metrics_timeseries.jsonl...")
count = 0
with open('data/instana/metrics_timeseries.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'metrics_timeseries.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/metrics_timeseries.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample timeseries keys: {list(sample.keys())}')
        if 'points' in sample:
            print(f'Points count: {len(sample["points"])}')

# Validate infrastructure_entities.jsonl
print("\nValidating infrastructure_entities.jsonl...")
count = 0
with open('data/instana/infrastructure_entities.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'infrastructure_entities.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/infrastructure_entities.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample entity keys: {list(sample.keys())}')
        if 'items' in sample:
            print(f'Items count: {len(sample["items"])}')
            if sample['items']:
                item = sample['items'][0]
                print(f'First item keys: {list(item.keys())}')

# Validate applications.jsonl
print("\nValidating applications.jsonl...")
count = 0
with open('data/instana/applications.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'applications.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/applications.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample application keys: {list(sample.keys())}')

# Validate endpoints.jsonl
print("\nValidating endpoints.jsonl...")
count = 0
with open('data/instana/endpoints.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'endpoints.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/endpoints.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample endpoint keys: {list(sample.keys())}')

# Validate issues.jsonl
print("\nValidating issues.jsonl...")
count = 0
with open('data/instana/issues.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'issues.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/issues.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample issue keys: {list(sample.keys())}')

# Cross-file consistency checks
print("\nCross-file consistency checks...")

# Load entity_ids from infrastructure_entities.jsonl
entity_ids = set()
with open('data/instana/infrastructure_entities.jsonl') as f:
    for line in f:
        data = json.loads(line)
        for item in data.get('items', []):
            entity_ids.add(item['entity_id'])

print(f'Found {len(entity_ids)} unique entity_ids in infrastructure_entities.jsonl')

# Check metrics_timeseries.jsonl entity_ids
missing_entities = set()
with open('data/instana/metrics_timeseries.jsonl') as f:
    for line in f:
        data = json.loads(line)
        eid = data.get('entity_id')
        if eid and eid not in entity_ids:
            missing_entities.add(eid)

if missing_entities:
    print(f'ERROR: Metrics timeseries reference non-existent entities: {missing_entities}')
else:
    print('All metrics timeseries entity_ids are valid.')

# Check issues.jsonl entity_ids
missing_entities_issues = set()
with open('data/instana/issues.jsonl') as f:
    for line in f:
        data = json.loads(line)
        eid = data.get('entity_id')
        if eid and eid not in entity_ids:
            missing_entities_issues.add(eid)

if missing_entities_issues:
    print(f'ERROR: Issues reference non-existent entities: {missing_entities_issues}')
else:
    print('All issues entity_ids are valid.')

print("\nValidation complete.")
