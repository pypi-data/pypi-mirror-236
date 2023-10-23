from setuptools import setup, find_packages
import os

requirements_path = "requirements.txt"

with open(requirements_path, "r") as f:
    dependencies = f.read().splitlines()

setup(
    include_package_data=True,
    name="SimpleApplication",
    version="1.0.8",
    description="Simple Application in Python",
    url='https://gitlab.com/carrivalegervasi/provacg.git',
    author="CarrivaleGervasi",
    packages=find_packages(), 
    install_requires=dependencies,
)
