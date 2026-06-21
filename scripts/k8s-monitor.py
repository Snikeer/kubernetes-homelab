# Importing Kubernetes client libraries
from kubernetes import client, config
from kubernetes.client.rest import ApiException



#coding emojis:https://emojidb.org/coding-emojis
#✅️❌🟢🔴⚠️ 



def load_cluster_config():
    """
    Loading Kubernetes configuration from the K3s kubeconfig file.
    This avoids relying on ~/.kube/config which is often not set in K3s.
    """
    try:
        # Explicitly point to K3s kubeconfig
        config.load_kube_config(config_file="/etc/rancher/k3s/k3s.yaml")

        print("✅ Successfully authenticated with Kubernetes cluster.")
        return True

    except Exception as e:
        print(f"❌ Failed to load Kubernetes configuration: {e}")
        return False


def monitor_cluster():
    """
    Retrieving all pods across all namespaces and verifying their status.
    """

    # Creating Kubernetes Core API client
    v1 = client.CoreV1Api()

    print("\n========================================")
    print("Alexanders - Cluster Health Check")
    print("========================================\n")

    try:
        # Retrieving all pods from all namespaces
        pods = v1.list_pod_for_all_namespaces(watch=False)

        healthy_count = 0
        unhealthy_count = 0

        # Iterating through each pod
        for pod in pods.items:

            pod_name = pod.metadata.name
            namespace = pod.metadata.namespace
            phase = pod.status.phase

            # Verifying container readiness if available
            container_ready = False

            if pod.status.container_statuses:
                container_ready = all(
                    container.ready
                    for container in pod.status.container_statuses
                )

            # A pod is considered healthy if:
            # - It is Running AND all containers are ready
            # - OR it has completed successfully (Jobs)
            if (phase == "Running" and container_ready) or phase == "Succeeded":

                healthy_count += 1

                print(
                    f"🟢 HEALTHY | Namespace: {namespace:<15} "
                    f"Pod: {pod_name}"
                )

            else:
                unhealthy_count += 1

                restart_count = 0

                if pod.status.container_statuses:
                    restart_count = sum(
                        container.restart_count
                        for container in pod.status.container_statuses
                    )

                print(
                    f"🔴 UNHEALTHY | Namespace: {namespace:<15} "
                    f"Pod: {pod_name}"
                )
                print(f"   Status: {phase}")
                print(f"   Restarts: {restart_count}")

        # Cluster summary
        print("\n========================================")
        print("Cluster Summary")
        print("========================================")
        print(f"Healthy Pods   : {healthy_count}")
        print(f"Unhealthy Pods : {unhealthy_count}")

        if unhealthy_count == 0:
            print("✅ Cluster health check passed.")
        else:
            print("⚠️ Cluster requires attention.")

    except ApiException as e:
        print(f"❌ Kubernetes API error: {e}")


def check_nodes():
    """
    Verify the status of all Kubernetes nodes.
    """

    v1 = client.CoreV1Api()

    print("\n========================================")
    print("Node Status")
    print("========================================")

    try:
        # Retrieving all nodes in the cluster
        nodes = v1.list_node()

        for node in nodes.items:

            node_name = node.metadata.name
            ready_status = "Unknown"

            # Finding the Ready condition for the node
            for condition in node.status.conditions:
                if condition.type == "Ready":
                    ready_status = condition.status

            if ready_status == "True":
                print(f"🟢 Node [{node_name}] is Ready")
            else:
                print(f"🔴 Node [{node_name}] is Not Ready")

    except ApiException as e:
        print(f"❌ Failed to retrieve node information: {e}")


if __name__ == "__main__":

    # Loading Kubernetes configuration
    if load_cluster_config():

        # Runing node health checks
        check_nodes()

        # also runing pod health checks
        monitor_cluster()
