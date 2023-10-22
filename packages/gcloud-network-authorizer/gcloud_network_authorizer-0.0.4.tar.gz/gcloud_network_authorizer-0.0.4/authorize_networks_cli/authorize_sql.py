# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
import os
import json
from typing import Any, Dict, List, Tuple
import requests

from .save_config import SqlConfig
from .util import AuthorizedIp, get_access_token, get_new_ip_entry


BASE_SQL_ADMIN_URL = (
    "https://sqladmin.googleapis.com/v1/projects/$projectName/instances"
)


def get_authorized_ips(
        cloud_instance: str,
        project_name: str) -> List[Dict[str, str]]:
    command = (
        "gcloud sql instances describe --project=$project_name $sql_instance"
        .replace(
            "$sql_instance", cloud_instance
        )
        .replace(
            "$project_name", project_name
        )
        + " --format=json | jq -r '"
        + ".settings.ipConfiguration.authorizedNetworks'"
    )
    result = os.popen(command).read()
    return json.loads(result)


def build_authorize_request(authorized_networks: List[AuthorizedIp]):
    settings_dict = {
        "settings": {
            "ipConfiguration": {
                "authorizedNetworks": [
                    {"name": ip.name, "value": ip.value}
                    for ip in authorized_networks
                ]
            }
        }
    }

    return settings_dict


def authorize_new_ips(
        ips: List[AuthorizedIp],
        instance_name: str,
        project_name: str) -> Tuple[int, Any]:
    token = get_access_token()
    json_request = build_authorize_request(ips)
    response = requests.patch(
        f"{BASE_SQL_ADMIN_URL}/{instance_name}"
        .replace("$projectName", project_name),
        json=json_request,
        headers={"Authorization": f"Bearer {token}"},
        timeout=10000,
    )
    return (response.status_code, response.json())


def authorize_sql_network(config: SqlConfig) -> Tuple[int, Any]:
    authorized_ips_string = get_authorized_ips(
        config.sql_instance_name,
        config.project_name)
    authorized_objects = [
        AuthorizedIp(d["name"], d["value"]) for d in authorized_ips_string
    ]
    network_changer = config.name_of_network_changer
    authorized_objects_without_me = list(
        filter(lambda a: a.name != network_changer, authorized_objects)
    )
    authorized_objects_without_me.append(
        get_new_ip_entry(config.name_of_network_changer))
    return authorize_new_ips(
        authorized_objects_without_me,
        config.sql_instance_name,
        config.project_name)
