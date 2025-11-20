import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_app_topology, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()

    topologies = []
    for i in range(args.count):
        topologies.append(gen_app_topology())

    write_jsonl("data/instana/app_topology.jsonl", topologies)

if __name__ == "__main__":
    main()
