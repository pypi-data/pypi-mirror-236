#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2016, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from py2neo import __author__, __email__, __license__, __package__, __version__


packages = find_packages(exclude=("book", "test", "test_ext", "test_ext.*"))
package_metadata = {
    "name": "py2neo-archive",
    "version": __version__,
    "description": "Python client library and toolkit for Neo4j",
    "long_description": "Py2neo is a client library and comprehensive toolkit for working with "
                        "Neo4j from within Python applications and from the command line. The "
                        "core library has no external dependencies and has been carefully "
                        "designed to be easy and intuitive to use.",
    "author": __author__,
    "author_email": __email__,
    "url": "http://py2neo.org/",
    "entry_points": {
        "console_scripts": [
            "py2neo = py2neo.__init__:main",
            "neokit = neokit:main",
            "geoff = py2neo.ext.geoff.__main__:main",
        ],
    },
    "packages": packages,
    "py_modules": ["neokit"],
    "license": __license__,
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Database",
        "Topic :: Software Development",
    ],
    "zip_safe": False,
}

setup(**package_metadata)
