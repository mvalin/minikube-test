from kubernetes.client.rest import ApiException
from kubernetes import client, config
from consolemenu import ConsoleMenu
from consolemenu.items import MenuItem, FunctionItem
from rich.console import Console


def get_pods(api_instance):
    return api_instance.list_pod_for_all_namespaces(watch=False).items


def get_logs(api_instance, pod):
    try:
        api_response = api_instance.read_namespaced_pod_log(
            name=pod.metadata.name, namespace=pod.metadata.namespace)
        print(api_response)
        with console.pager():
            console.print(api_response)
    except ApiException as e:
        print(f'Found exception in reading the logs: {e.reason}')


def menu_pods(api_instance, pods):
    menu = ConsoleMenu("Select Pod", "Get logs", clear_screen=False)
    MenuItem("Menu Item")
    for p in pods:
        item_str = f"{p.status.pod_ip: <16}{p.metadata.namespace: <21}"\
            f"{p.metadata.name:}"
        function_item = FunctionItem(item_str, get_logs, [api_instance, p])
        menu.append_item(function_item)

    menu.show()


def main():
    config.load_kube_config()
    api_instance = client.CoreV1Api()

    pods = get_pods(api_instance)

    menu_pods(api_instance, pods)


if __name__ == "__main__":
    console = Console()
    main()
