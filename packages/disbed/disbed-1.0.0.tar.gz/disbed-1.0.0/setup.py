from setuptools import setup, find_packages

setup(
    name="disbed",
    version="1.0.0",
    packages=find_packages(include=["disbed*"]),  # Include only packages that start with "custerm"
    install_requires=[],
)
