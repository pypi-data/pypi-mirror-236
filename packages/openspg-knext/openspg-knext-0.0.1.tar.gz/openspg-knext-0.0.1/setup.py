# -*- coding: utf-8 -*-

#  Copyright 2023 AntGroup CO., Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
#  in compliance with the License. You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied.

import os
from string import Template

from setuptools import setup, find_packages

cwd = os.path.abspath(os.path.dirname(__file__))
# Read Version
with open(os.path.join(cwd, "KNEXT_VERSION"), "r") as rf:
    version = rf.readline().strip("\n").strip()

# Generate knext.__init__.py
with open(os.path.join(cwd, "knext/version.py"), "w") as wf:
    content = Template(
        """
__version__ = "${VERSION}"
    """
    ).substitute(
        VERSION=version,
    )
    wf.write(content)

setup(
    name="openspg-knext",
    version=version,
    description="knext",
    author="jier",
    author_email="qy266141@antgroup.com",
    packages=find_packages(
        where=".",
        exclude=[
            ".*test.py",
            "*_test.py",
            "*_debug.py",
            "*.txt",
            "tests",
            "tests.*",
            "configs",
            "configs.*",
            "test",
            "test.*",
            "*.tests",
            "*.tests.*",
            "*.pyc",
        ]
    ),
    python_requires='>=3.8',
    install_requires=[
        r.strip()
        for r in open("requirements.txt", "r")
        if not r.strip().startswith("#")
    ],
    entry_points={
        "console_scripts": [
            "knext=knext.client.knext_cli:_main",
        ]
    },
    include_package_data=True,
    package_data={
        "bin": ["*"],
    },
)
