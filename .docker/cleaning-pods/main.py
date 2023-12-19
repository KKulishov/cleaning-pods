from kubernetes import client, config
from kubernetes.client.rest import ApiException

def get_all_evicted_pods(api_instance):
    all_evicted_pods = []
    try:
        namespaces = api_instance.list_namespace().items
        for namespace in namespaces:
            pods = api_instance.list_namespaced_pod(namespace.metadata.name, field_selector="status.phase=Failed")
            evicted_pods = [pod.metadata.name for pod in pods.items if pod.status.phase == "Failed"]
            all_evicted_pods.extend([(namespace.metadata.name, pod) for pod in evicted_pods])
        return all_evicted_pods
    except ApiException as e:
        print(f"Exception when calling CoreV1Api: {e}")
        return []

def delete_evicted_pods(api_instance, evicted_pods):
    for namespace, pod_name in evicted_pods:
        try:
            api_instance.delete_namespaced_pod(pod_name, namespace)
            print(f"Pod {pod_name} in namespace {namespace} deleted successfully.")
        except ApiException as e:
            print(f"Exception when calling CoreV1Api->delete_namespaced_pod: {e}")

def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    evicted_pods = get_all_evicted_pods(v1)

    if evicted_pods:
        print(f"Found {len(evicted_pods)} evicted pod(s) in the cluster. Deleting...")
        delete_evicted_pods(v1, evicted_pods)
    else:
        print("No evicted pods found.")

if __name__ == "__main__":
    main()