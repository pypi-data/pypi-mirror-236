import click
from .authorize_kubernetes import authorize_kubernetes_network
from .authorize_sql import authorize_sql_network

from .save_config import KubernetesEngineConfig, SqlConfig, \
    load_kubernetes_config, \
    load_sql_config, save_kubernetes_config, save_sql_config
from .util import add_commands


@click.group(name="cli")
def cli():
    """
    This is the main command-line interface
    for managing network authorizations.
    It provides commands to authorize Kubernetes
    and SQL networks and to save their configurations.
    """
    pass


@click.command(name="authorize_kubernetes")
def authorize_kubernetes():
    """
    Authorize Kubernetes network
    access based on the previously saved configuration.
    """
    config = load_kubernetes_config()
    print(authorize_kubernetes_network(config))


@click.command(name="authorize_sql")
def authorize_sql():
    """
    Authorize SQL network access based
    on the previously saved configuration.
    """
    config = load_sql_config()
    print(authorize_sql_network(config))


@click.command(name="kubernetes_save")
@click.option(
    '--name',
    required=True,
    type=str,
    help='Network user name')
@click.option(
    '--kubernetes_instance',
    required=True,
    type=str,
    help='Kubernetes instance name')
@click.option(
    '--project_name',
    required=True,
    type=str,
    help='Base project name')
@click.option(
    '--zone',
    required=True,
    type=str,
    help='Kubernetes zone')
def set_kubernetes_config(
    name: str,
    kubernetes_instance: str,
    zone: str,
        project_name: str):
    """
    Save Kubernetes configuration for authorizing network access.
    This command allows you to set up
    the configuration required to authorize Kubernetes network access.
    """
    save_kubernetes_config(KubernetesEngineConfig(
        kubernetes_instance, name, project_name, zone))


@click.command(name="sql_save")
@click.option(
    '--name',
    required=True,
    type=str,
    help='Network user name')
@click.option(
    '--sql_instance',
    required=True,
    type=str,
    help='SQL instance name')
@click.option(
    '--project_name',
    required=True,
    type=str,
    help='Base project name')
def set_sql_config(name: str, sql_instance: str, project_name: str):
    """
    Save SQL configuration for authorizing network access.
    This command allows you to set up
    the configuration required to authorize SQL network access.
    """
    save_sql_config(SqlConfig(sql_instance, name, project_name))


add_commands(
    cli,
    set_kubernetes_config,
    set_sql_config,
    authorize_kubernetes,
    authorize_sql)

if __name__ == '__main__':
    cli()
