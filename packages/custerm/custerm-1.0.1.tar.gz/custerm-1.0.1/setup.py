from setuptools import setup, find_packages

setup(
    name="custerm",
    version="1.0.1",
    packages=find_packages(include=["custerm*"]),  # Include only packages that start with "custerm"
    install_requires=[],
)
