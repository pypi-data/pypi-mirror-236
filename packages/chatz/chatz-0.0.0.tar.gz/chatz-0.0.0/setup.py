from setuptools import setup, find_packages

setup(
    name="chatz",
    version="0.0.0",
    description="Chatz python library",
    author="Chatz Team",
    author_email="silveryfu@gmail.com",
    license="Apache License, Version 2.0",
    packages=find_packages(exclude=("tests",)),
    python_requires='>=3.8',
    include_package_data=True,
    install_requires = open('requirements.txt').readlines(),
)
