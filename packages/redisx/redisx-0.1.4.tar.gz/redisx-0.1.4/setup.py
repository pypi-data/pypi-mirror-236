#!/usr/bin/env python
from setuptools import setup

setup(
    name="redisx",
    description="Python client for RedisX",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    version="0.1.4",
    license="MIT",
    url="https://github.com/weedge/redisx-py",
    author="weedge",
    author_email="weege007@gmail.com",
    python_requires=">=3.10",
    packages=["redisx"],
    install_requires=["redis == 5.0.0"],
)
