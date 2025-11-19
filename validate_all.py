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
with open('data/instana/infrastructure_entities.jsonl', 'r') as f:
    data = json.load(f)
    count = len(data.get('items', []))
print(f'infrastructure_entities.jsonl: Valid JSON, item count: {count}')
if count > 0:
    print(f'Sample entity keys: {list(data.keys())}')
    if data.get('items'):
        print(f'First item keys: {list(data["items"][0].keys())}')

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
    data = json.load(f)
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

# Validate infra_topology.jsonl
print("\nValidating infra_topology.jsonl...")
count = 0
with open('data/instana/infra_topology.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'infra_topology.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/infra_topology.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample topology keys: {list(sample.keys())}')
        if 'nodes' in sample:
            print(f'Nodes count: {len(sample["nodes"])}')
        if 'edges' in sample:
            print(f'Edges count: {len(sample["edges"])}')

# Validate app_topology.jsonl
print("\nValidating app_topology.jsonl...")
count = 0
with open('data/instana/app_topology.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'app_topology.jsonl: Valid JSON, count: {count}')

# Validate alert_configs.jsonl
print("\nValidating alert_configs.jsonl...")
count = 0
with open('data/instana/alert_configs.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'alert_configs.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/alert_configs.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample alert keys: {list(sample.keys())}')

# Validate metrics_catalog.jsonl
print("\nValidating metrics_catalog.jsonl...")
count = 0
with open('data/instana/metrics_catalog.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'metrics_catalog.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/metrics_catalog.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample catalog keys: {list(sample.keys())}')
        if 'metrics' in sample:
            print(f'Metrics count: {len(sample["metrics"])}')

# Validate entity_types.jsonl
print("\nValidating entity_types.jsonl...")
count = 0
with open('data/instana/entity_types.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'entity_types.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/entity_types.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample types keys: {list(sample.keys())}')
        if 'entity_types' in sample:
            print(f'Types count: {len(sample["entity_types"])}')

# Cross-file consistency for topology
print("\nCross-file consistency for topology...")
topo_entity_ids = set()
with open('data/instana/infra_topology.jsonl') as f:
    for line in f:
        data = json.loads(line)
        for node in data.get('nodes', []):
            topo_entity_ids.add(node['id'])

missing_topo = topo_entity_ids - entity_ids
if missing_topo:
    print(f'ERROR: Topology nodes reference non-existent entities: {missing_topo}')
else:
    print('All topology node IDs are valid.')

# Cross-file consistency for alerts
alert_entity_ids = set()
with open('data/instana/alert_configs.jsonl') as f:
    for line in f:
        data = json.loads(line)
        if 'entity_id' in data:
            alert_entity_ids.add(data['entity_id'])

missing_alerts = alert_entity_ids - entity_ids
if missing_alerts:
    print(f'ERROR: Alert configs reference non-existent entities: {missing_alerts}')
else:
    print('All alert config entity_ids are valid.')

# Validate website_config.jsonl
print("\nValidating website_config.jsonl...")
count = 0
with open('data/instana/website_config.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'website_config.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/website_config.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample website config keys: {list(sample.keys())}')

# Validate website_catalog.jsonl
print("\nValidating website_catalog.jsonl...")
count = 0
with open('data/instana/website_catalog.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'website_catalog.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/website_catalog.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample website catalog keys: {list(sample.keys())}')
        if 'websites' in sample:
            print(f'Websites count: {len(sample["websites"])}')

# Validate website_metrics.jsonl
print("\nValidating website_metrics.jsonl...")
count = 0
with open('data/instana/website_metrics.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'website_metrics.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/website_metrics.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample website metrics keys: {list(sample.keys())}')
        if 'points' in sample:
            print(f'Points count: {len(sample["points"])}')

# Validate website_analyze.jsonl
print("\nValidating website_analyze.jsonl...")
count = 0
with open('data/instana/website_analyze.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'website_analyze.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/website_analyze.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample website analyze keys: {list(sample.keys())}')

# Validate logs.jsonl
print("\nValidating logs.jsonl...")
count = 0
with open('data/instana/logs.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'logs.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/logs.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample log keys: {list(sample.keys())}')

# Validate synthetic_checks.jsonl
print("\nValidating synthetic_checks.jsonl...")
count = 0
with open('data/instana/synthetic_checks.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'synthetic_checks.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/synthetic_checks.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample synthetic check keys: {list(sample.keys())}')

# Validate synthetic_runs.jsonl
print("\nValidating synthetic_runs.jsonl...")
count = 0
with open('data/instana/synthetic_runs.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'synthetic_runs.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/synthetic_runs.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample synthetic run keys: {list(sample.keys())}')

# Cross-file consistency for synthetic checks and runs
print("\nCross-file consistency for synthetic checks and runs...")
check_ids = set()
with open('data/instana/synthetic_checks.jsonl') as f:
    for line in f:
        data = json.loads(line)
        check_ids.add(data['check_id'])

missing_runs = set()
with open('data/instana/synthetic_runs.jsonl') as f:
    for line in f:
        data = json.loads(line)
        cid = data.get('check_id')
        if cid and cid not in check_ids:
            missing_runs.add(cid)

if missing_runs:
    print(f'ERROR: Synthetic runs reference non-existent checks: {missing_runs}')
else:
    print('All synthetic runs reference valid checks.')

# Validate mobile_config.jsonl
print("\nValidating mobile_config.jsonl...")
count = 0
with open('data/instana/mobile_config.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'mobile_config.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/mobile_config.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample mobile config keys: {list(sample.keys())}')

# Validate mobile_catalog.jsonl
print("\nValidating mobile_catalog.jsonl...")
count = 0
with open('data/instana/mobile_catalog.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'mobile_catalog.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/mobile_catalog.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample mobile catalog keys: {list(sample.keys())}')
        if 'mobile_apps' in sample:
            print(f'Mobile apps count: {len(sample["mobile_apps"])}')

# Validate mobile_metrics.jsonl
print("\nValidating mobile_metrics.jsonl...")
count = 0
with open('data/instana/mobile_metrics.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'mobile_metrics.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/mobile_metrics.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample mobile metrics keys: {list(sample.keys())}')
        if 'points' in sample:
            print(f'Points count: {len(sample["points"])}')

# Validate mobile_analyze.jsonl
print("\nValidating mobile_analyze.jsonl...")
count = 0
with open('data/instana/mobile_analyze.jsonl') as f:
    for line in f:
        json.loads(line)
        count += 1
print(f'mobile_analyze.jsonl: Valid JSON, count: {count}')
if count > 0:
    with open('data/instana/mobile_analyze.jsonl') as f:
        sample = json.loads(next(f))
        print(f'Sample mobile analyze keys: {list(sample.keys())}')

print("\nValidation complete.")
