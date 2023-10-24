from setuptools import find_packages, setup

setup(
    name='drug_repurposing_extract',
    packages=find_packages(include=["drug_repurposing"]),
    version='0.1.2',
    description='Library for automatic generation of drug repurposing data',
    author='Shiva Aryal',
)