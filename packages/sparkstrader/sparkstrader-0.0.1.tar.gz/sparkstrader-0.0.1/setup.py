#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2023/7/22 22:09
Desc: PYPI info file
"""
import re
import ast

import setuptools

from sparkstrader import __version__, __author__, __authoremail__

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

requirementsPath = "requirements.txt"

requirementslist = []
f = open(requirementsPath, "r")
for line in f:
    requirementslist.append(str.strip(line))
f.close()
# print(requirementslist)

# print(__version__)
# print(__author__)
# print(__authoremail__)


setuptools.setup(
    name="sparkstrader",
    version=__version__,
    author=__author__,
    author_email=__authoremail__,
    license="MIT",
    description="python api for sparkstrader.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yacper/sparks_api_py",
    packages=setuptools.find_packages(),
    install_requires=requirementslist,
    package_data={"": ["*.py", "*.json", "*.pk", "*.js", "*.zip"]},
    keywords=[
        "stock",
        "option",
        "futures",
        "fund",
        "bond",
        "index",
        "air",
        "finance",
        "spider",
        "quant",
        "quantitative",
        "investment",
        "trading",
        "algotrading",
        "data",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
