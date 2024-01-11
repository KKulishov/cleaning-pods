from kubernetes import client, config
from kubernetes.client.rest import ApiException
from prometheus_client import Gauge, push_to_gateway, CollectorRegistry
import os
import requests
from datetime import datetime

Exception_ns = os.getenv("Exception_ns").split(',')
PROMETHEUS_GATEWAY = os.getenv("PROMETHEUS_GATEWAY", "prometheus-pushgateway.monitoring:9091")
PROMETHEUS_JOB_NAME = 'cleaning-faileds-pods'
PUSHGATEWAY_IS_TRUE = os.getenv("PUSHGATEWAY_IS_TRUE", False)

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

def get_all_evicted_pods(api_instance):
    all_evicted_pods = []
    try:
        namespaces = api_instance.list_namespace().items
        for namespace in namespaces:
            if namespace.metadata.name in Exception_ns:
                print(f"{formatted_time} Skipping namespace {namespace.metadata.name} as it's in the exception list.")
                continue
            pods = api_instance.list_namespaced_pod(namespace.metadata.name, field_selector="status.phase=Failed")
            for pod in pods.items:
                if pod.metadata.labels and pod.metadata.labels.get("untouchable") == "true":
                    # Пропускаем под с меткой "untouchable=true"
                    print(f"{formatted_time} Skipping pod {pod.metadata.name} in namespace {namespace.metadata.name} as it's untouchable.")
                    continue
                if pod.status.phase == "Failed":
                    all_evicted_pods.append((namespace.metadata.name, pod.metadata.name))
            #evicted_pods = [pod.metadata.name for pod in pods.items if pod.status.phase == "Failed"]
            #all_evicted_pods.extend([(namespace.metadata.name, pod) for pod in evicted_pods])
        return all_evicted_pods
    except ApiException as e:
        print(f"Exception when calling CoreV1Api: {e}")
        return []

def delete_evicted_pods(api_instance, evicted_pods):
    deleted_pods_count = 0
    for namespace, pod_name in evicted_pods:
        try:
            api_instance.delete_namespaced_pod(pod_name, namespace)
            deleted_pods_count += 1
            print(f"{formatted_time} Pod {pod_name} in namespace {namespace} deleted successfully.")
        except ApiException as e:
            print(f"{formatted_time} Exception when calling CoreV1Api->delete_namespaced_pod: {e}")
    
    return deleted_pods_count, namespace

def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    evicted_pods = get_all_evicted_pods(v1)

    ## чистка старых метрик job 
    response = requests.delete(f'http://{PROMETHEUS_GATEWAY}/metrics/job/{PROMETHEUS_JOB_NAME}')
    if response.status_code == 202:
        print(f'{formatted_time} Deleted metrics for job {PROMETHEUS_JOB_NAME}')
    else:
        print(f'{formatted_time} Failed to delete metrics. Status code: {response.status_code}')
        print(response.text)

    ## чистка подов && отправка метрик в Pushgateway
    if evicted_pods:
        print(f"{formatted_time} Found {len(evicted_pods)} evicted pod(s) in the cluster. Deleting...")
        deleted_count = delete_evicted_pods(v1, evicted_pods)
        # Отправка метрики в Prometheus Pushgateway
        if PUSHGATEWAY_IS_TRUE == True:
            registry = CollectorRegistry()
            g = Gauge('deleted_pods_count', 'Count of deleted pods', ['namespace_cleaning', 'test'], registry=registry)
            g.labels(namespace_cleaning=deleted_count[1], test='label_test').set(deleted_count[0])
            push_to_gateway(PROMETHEUS_GATEWAY, job=PROMETHEUS_JOB_NAME, registry=registry)
            print(f"{formatted_time} Deleted pods count metric sent to Prometheus Pushgateway.")
    else:
        print(f"{formatted_time} No evicted pods found.")

if __name__ == "__main__":
    main()