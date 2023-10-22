from dataclasses import dataclass
import os
from typing import Dict
import requests
from click import Command, Group

IP_RESOLVE_API = "https://api.ipify.org"


@dataclass
class AuthorizedIp:
    name: str
    value: str


def get_ipv4() -> str:
    data = requests.get(IP_RESOLVE_API, timeout=1000)
    return f"{data.text}/32"    


def get_new_ip_entry(name: str) -> AuthorizedIp:
    return AuthorizedIp(name, get_ipv4())


def add_commands(group: Group, *args: Command):
    for arg in args:
        group.add_command(arg)


def get_access_token() -> str:
    return os.popen("gcloud auth print-access-token").read().strip()


def replace_with_map(input: str, replacements: Dict[str, str]) -> str:
    value_to_return = input
    for key, value in replacements.items():
        value_to_return = value_to_return.replace(key, value)
    return value_to_return
