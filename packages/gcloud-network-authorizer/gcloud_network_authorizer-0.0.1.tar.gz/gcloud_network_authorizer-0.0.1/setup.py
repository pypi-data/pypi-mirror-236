from setuptools import setup, find_packages


setup(
    name="gcloud_network_authorizer",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["click", "requests"],
    entry_points={
        "console_scripts": ["authorize_networks=authorize_networks_cli.main:cli"],
    },
)
