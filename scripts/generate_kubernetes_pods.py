import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import gen_kubernetes_pod, write_jsonl

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=150, help="Number of pods to generate")
    parser.add_argument("--clusters", type=int, default=10, help="Number of clusters to distribute pods across")
    parser.add_argument("--deployments-per-cluster", type=int, default=5, help="Number of deployments per cluster")
    args = parser.parse_args()

    pods = []
    for i in range(args.count):
        cluster_id = f"k8s-cluster-{i % args.clusters}"
        deployment_id = f"deploy-{(i // (args.count // (args.clusters * args.deployments_per_cluster))) % args.deployments_per_cluster}"
        pods.append(gen_kubernetes_pod(i, cluster_id, deployment_id))

    write_jsonl("data/instana/kubernetes_pods.jsonl", pods)
    print(f"Generated {len(pods)} pods.")

if __name__ == "__main__":
    main()
