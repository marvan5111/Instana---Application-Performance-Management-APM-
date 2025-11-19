import json

print('Testing configuration files...')
try:
    with open('data/instana/website_config.jsonl', 'r') as f:
        website_config = [json.loads(line) for line in f]
    print(f' Website config loaded: {len(website_config)} entries from .jsonl')

    with open('data/instana/synthetic_checks.jsonl', 'r') as f:
        synthetic_config = [json.loads(line) for line in f]
    print(f' Synthetic checks loaded: {len(synthetic_config)} entries from .jsonl')

    with open('data/instana/alert_configs.jsonl', 'r') as f:
        alert_config = [json.loads(line) for line in f]
    print(f' Alert configs loaded: {len(alert_config)} entries from .jsonl')

except Exception as e:
    print(f' Config error: {e}')
