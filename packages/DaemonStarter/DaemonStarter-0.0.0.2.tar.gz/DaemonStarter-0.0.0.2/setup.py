#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="DaemonStarter",
    version="0.0.0.2",
    author="XiaoCao",
    author_email="inflowers@126.com",
    description="a Daemon Starter",
    long_description=open("readme.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://pypi.python.org/pypi/DaemonStarter",
    packages=find_packages(exclude=["*.*"]),
    include_package_data=True,
    py_modules=[],
    install_requires=[
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
