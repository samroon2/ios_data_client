import sys
from setuptools import setup, find_packages
from setuptools.command.install import install
import distutils.command.install as dist_inst

with open("README.md") as readme:
    long_description = readme.read()

PACKAGE_DATA = {"": ["*.csv", "*.pickle"]}

setup(
    name="ios_data_client",
    version="0.0.1",
    description="Client for getting app data found on the ios app store.",
    packages=find_packages(),
    package_data=PACKAGE_DATA,
    python_requires=">=3.6.1",
    install_requirements=[
        "sumy>=0.7.0",
        "requests>=2.18.4",
        "beautifulsoup4>=4.9.3"
    ]
)