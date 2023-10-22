from setuptools import setup, find_packages

MARKDOWN_PATH = "./resources/long_description.txt"

with open(MARKDOWN_PATH, "r", encoding="utf-8") as file:
    text = file.read()
    setup(
        name="gcloud_network_authorizer",
        version="0.0.6",
        long_description=text,
        packages=find_packages(),
        install_requires=["click", "requests"],
        entry_points={
            "console_scripts": ["authorize_networks=authorize_networks_cli.main:cli"],
        },
    )
