import argparse
import sys
sys.path.insert(0, '.')
from instana_synthetic.generators import (
    gen_kubernetes_cluster,
    gen_kubernetes_deployment,
    gen_kubernetes_pod,
    write_jsonl
)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clusters", type=int, default=10, help="Number of clusters to generate")
    parser.add_argument("--deployments-per-cluster", type=int, default=5, help="Number of deployments per cluster")
    parser.add_argument("--pods-per-deployment", type=int, default=3, help="Number of pods per deployment")
    parser.add_argument("--tenants", type=int, default=1, help="Number of tenants to generate data for")
    args = parser.parse_args()
 
    all_clusters = []
    all_deployments = []
    all_pods = []

    for t in range(args.tenants):
        tenant_id = f"tenant-{t+1}"
        clusters = [gen_kubernetes_cluster(i) for i in range(args.clusters)]
        deployments = [gen_kubernetes_deployment(i, c['cluster_id']) for c in clusters for i in range(args.deployments_per_cluster)]
        pods = [gen_kubernetes_pod(i, d['cluster_id'], d['deployment_id']) for d in deployments for i in range(args.pods_per_deployment)]
        all_clusters.extend(clusters)
        all_deployments.extend(deployments)
        all_pods.extend(pods)

    write_jsonl("data/instana/kubernetes_clusters.jsonl", all_clusters)
    write_jsonl("data/instana/kubernetes_deployments.jsonl", all_deployments)
    write_jsonl("data/instana/kubernetes_pods.jsonl", all_pods)
    print(f"Generated {len(all_clusters)} clusters, {len(all_deployments)} deployments, and {len(all_pods)} pods across {args.tenants} tenants.")

if __name__ == "__main__":
    main()
