 import json
 import yaml
 from typing import List, Dict
 
 def generate_pod_manifest(pod_data: Dict) -> Dict:
     """Generate a Kubernetes Pod manifest from synthetic data."""
     return {
         "apiVersion": "v1",
         "kind": "Pod",
         "metadata": {
             "name": pod_data.get("name", "default-pod"),
             "namespace": pod_data.get("namespace", "default"),
             "labels": pod_data.get("labels", {})
         },
         "spec": {
             "containers": [
                 {
                     "name": container.get("name"),
                     "image": container.get("image"),
                     "ports": [{"containerPort": 80}]
                 } for container in pod_data.get("containers", [])
             ]
         }
     }
 
 def export_to_yaml(manifests: List[Dict], output_file: str):
     """Export a list of Kubernetes manifests to a single YAML file."""
     try:
         with open(output_file, 'w') as f:
             yaml.dump_all(manifests, f, sort_keys=False)
         print(f"Successfully exported {len(manifests)} manifests to {output_file}")
     except Exception as e:
         print(f"Error exporting to YAML: {e}")
 
 if __name__ == "__main__":
     # Example Usage
     from instana_synthetic.generators import gen_kubernetes_pod
     pods = [gen_kubernetes_pod(i) for i in range(3)]
     manifests = [generate_pod_manifest(p) for p in pods]
     export_to_yaml(manifests, "data/exports/kubernetes_manifests.yaml")