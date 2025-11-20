import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_kubernetes_deployment, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=50, help="Number of deployments to generate")
    parser.add_argument("--clusters", type=int, default=10, help="Number of clusters to distribute deployments across")
    args = parser.parse_args()

    deployments = []
    for i in range(args.count):
        cluster_id = f"k8s-cluster-{i % args.clusters}"
        deployments.append(gen_kubernetes_deployment(i, cluster_id))

    write_jsonl("data/instana/kubernetes_deployments.jsonl", deployments)
    print(f"Generated {len(deployments)} deployments.")

if __name__ == "__main__":
    main()
