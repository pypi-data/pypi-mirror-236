from setuptools import find_packages, setup

packages = find_packages(exclude=("setup", "tests"))

version = "0.0.1"

setup(
    name="bipedal",
    version=version,
    description="Bioinformatics Pipelines for Experimental Data Analysis",
)
