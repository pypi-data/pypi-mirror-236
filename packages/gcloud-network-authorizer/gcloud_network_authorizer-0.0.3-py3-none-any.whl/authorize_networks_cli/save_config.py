# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring


from dataclasses import dataclass
import dataclasses
import json
import os
from typing import Any
SQL_CONFIG_PATH = "sql-config.json"
KUBERNETES_CONFIG_PATH = "kubernetes-config.json"


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def write_file(path: str, data: str):
    with open(path, 'w', encoding="utf-8") as file:
        file.write(data)


def read_file_as_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.loads(file.read())


@dataclass
class SqlConfig:
    sql_instance_name: str
    name_of_network_changer: str
    project_name: str


@dataclass
class KubernetesEngineConfig:
    kubernetes_instance_name: str
    name_of_network_changer: str
    project_name: str
    zone: str


def current_dir_path(path: str) -> str:
    package_dir = os.path.dirname(__file__)
    return os.path.join(package_dir, path)


def save_sql_config(sql_config: SqlConfig):
    json_config = json.dumps(sql_config, cls=EnhancedJSONEncoder, indent=4)
    write_file(current_dir_path(SQL_CONFIG_PATH), json_config)


def save_kubernetes_config(kubernetes_config: KubernetesEngineConfig):
    json_config = json.dumps(
        kubernetes_config,
        cls=EnhancedJSONEncoder,
        indent=4)
    write_file(current_dir_path(KUBERNETES_CONFIG_PATH), json_config)


def load_sql_config() -> SqlConfig:
    data = read_file_as_json(current_dir_path(SQL_CONFIG_PATH))
    return SqlConfig(**data)


def load_kubernetes_config() -> KubernetesEngineConfig:
    data = read_file_as_json(current_dir_path(KUBERNETES_CONFIG_PATH))
    return KubernetesEngineConfig(**data)
