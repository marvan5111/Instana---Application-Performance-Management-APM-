import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_host_agent_status, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=20)
    args = parser.parse_args()

    agents = []
    for i in range(args.count):
        agents.append(gen_host_agent_status())

    write_jsonl("data/instana/host_agent_status.jsonl", agents)

if __name__ == "__main__":
    main()
