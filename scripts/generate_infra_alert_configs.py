import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_infra_alert_config, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()

    configs = []
    for i in range(args.count):
        configs.append(gen_infra_alert_config())

    write_jsonl("data/instana/infra_alert_configs.jsonl", configs)

if __name__ == "__main__":
    main()
