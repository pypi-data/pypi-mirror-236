from typing import Any, List, Tuple
import requests
from .save_config import KubernetesEngineConfig

from .util import AuthorizedIp, get_access_token, \
    get_new_ip_entry, replace_with_map

BASE_URL = "https://container.googleapis.com/v1/" \
    + "projects/projectId/zones/zoneId/clusters/clusterId"


def get_authorized_networks(
       config: KubernetesEngineConfig) -> List[AuthorizedIp]:
    authorized_ips: List[AuthorizedIp] = []
    token = get_access_token()
    url = build_url(BASE_URL, config)
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    json_data = response.json()
    networks = json_data["masterAuthorizedNetworksConfig"]["cidrBlocks"]
    for network in networks:
        authorized_ips.append(
            AuthorizedIp(network.get("displayName"), network.get("cidrBlock"))
        )
    return authorized_ips


def build_authorize_request(
    config: KubernetesEngineConfig, ips: List[AuthorizedIp]
) -> Any:
    return {
        "name": f"projects/{config.project_name}"
        + f"/locations/{config.zone}"
        + f"/clusters/{config.kubernetes_instance_name}",
        "update": {
            "desiredMasterAuthorizedNetworksConfig": {
                "enabled": True,
                "cidrBlocks":
                [{"displayName": x.name, "cidrBlock": x.value} for x in ips],
                "gcpPublicCidrsAccessEnabled": False,
            }
        },
    }


def build_url(base_url: str, kubernetes_config: KubernetesEngineConfig) -> str:
    config_data = {"projectId": kubernetes_config.project_name,
                   "clusterId": kubernetes_config.kubernetes_instance_name,
                   "zoneId": kubernetes_config.zone}
    return replace_with_map(base_url, config_data)


def send_request_to_update_network(
    config: KubernetesEngineConfig, networks: List[AuthorizedIp]
):
    token = get_access_token()
    json_request = build_authorize_request(config, networks)
    response = requests.put(
        build_url(BASE_URL, config),
        json=json_request,
        headers={"Authorization": f"Bearer {token}"},
        timeout=10000,
    )
    return (response.status_code, response.json())


def authorize_kubernetes_network(
        kubernetes_config: KubernetesEngineConfig) -> Tuple[int, Any]:
    # TODO: check on destructuring eventually
    author = kubernetes_config.name_of_network_changer
    versions = get_authorized_networks(kubernetes_config)
    remove_me_versions = list(filter(lambda a: a.name != author, versions))
    remove_me_versions.append(get_new_ip_entry(author))
    return send_request_to_update_network(
        kubernetes_config,
        remove_me_versions)
