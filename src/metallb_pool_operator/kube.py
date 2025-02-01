from collections.abc import Sequence

from kubernetes import client, config


def patch_ipv6_pool(name: str, namespace: str, new_addresses: Sequence[str]) -> None:
    config.load_incluster_config()
    api = client.CustomObjectsApi()

    patch = {"spec": {"addresses": new_addresses}}
    api.patch_namespaced_custom_object(
        group="metallb.io",
        version="v1beta1",
        plural="ipaddresspools",
        namespace=namespace,
        name=name,
        body=patch,
    )
