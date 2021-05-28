#!/usr/bin/env python
# Copyright 2021 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# python setup.py sdist
# python setup.py bdist_wheel
# twine upload --skip-existing dist/*

__version__ = '0.0.1'

import os
import glob
import shutil
import tempfile
import subprocess
from pathlib import Path

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

here = os.path.abspath(os.path.dirname(__file__))
def read(filename):
    with open(os.path.join(here, filename), 'r') as fh:
        return fh.read()

def read_list(filename):
    return [l for l in read(filename).split('\n')
              if l.strip() != '' and not l.startswith('#')]

### SPDB Resource File Download ###
with tempfile.TemporaryDirectory() as tmp_dir:
    # TODO: Change to integration branch once merged
    command = ["git", "clone", "-q", "-b", "cvdb-support", "https://github.com/jhuapl-boss/spdb.git", tmp_dir]
    ret = subprocess.run(command, capture_output=True)
    if ret.returncode != 0:
        raise ChildProcessError(f"Error cloning SPDB: {ret.stderr}")
    src_path = Path(tmp_dir) / 'spdb' / 'project'
    dest_path = Path(__file__).resolve().parent / 'project'
    shutil.copytree(str(src_path), str(dest_path))


setup(
    name='cvdb',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/jhuapl-boss/cvdb',
    license="Apache Software License 2.0",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    setup_requires=['wheel'],
    tests_require=read_list('requirements-test.txt'),
    install_requires=read_list('requirements.txt'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=[
        'boss',
        'microns',
    ],
)

### Clean-up ###
shutil.rmtree(dest_path)