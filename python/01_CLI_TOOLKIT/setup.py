from setuptools import setup, find_packages

setup(
    name="hello-cli-toolkit",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click"
    ],
    entry_points={
        "console_scripts": [
            "hello-cli=hello_cli.cli:cli",
        ],
    },
)
