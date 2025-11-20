import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_kubernetes_cluster, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10, help="Number of clusters to generate")
    args = parser.parse_args()

    clusters = [gen_kubernetes_cluster(i) for i in range(args.count)]
    write_jsonl("data/instana/kubernetes_clusters.jsonl", clusters)
    print(f"Generated {len(clusters)} clusters.")

if __name__ == "__main__":
    main()
