from __future__ import absolute_import, division, print_function
from setuptools import setup, find_packages
import os
from os.path import isdir, isfile
import glob


# Makes setup work inside of a virtualenv
use_system_lib = True
if os.environ.get("BUILD_LIB") == "1":
    use_system_lib = False


base_dir = os.path.dirname(__file__)

__author__ = "Wu Haifeng"
__email__ = "wuhaifengdhu@163.com"

# Change this line to the module name you want to create
__title__ = "pyshifu"
__version__ = "0.0.9"
__summary__ = "An end-to-end machine learning and data mining framework on Hadoop."
__uri__ = "https://github.com/shifuml/pyshifu"

__requirements__ = [
    'six>=1.11.0'
]


def get_shifu_package_data():
    _data_files = add_recursively('pyshifu/java/')
    return _data_files


with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()


def add_recursively(directory):
    _data_files = {}
    if not directory.endswith("/"):
        directory += "/"
    items = glob.glob(directory + '*')
    _files = []
    _dirs = []
    for item in items:
        if isfile(item):
            _files.append(item)
        elif isdir(item):
            _dirs.append(item)
    _data_files[directory] = _files
    for _dir in _dirs:
        _data_files.update(add_recursively(_dir))
    return _data_files


setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    package_data=get_shifu_package_data(),
    author=__author__,
    author_email=__email__,
    url=__uri__,
    zip_safe=False,
    install_requires=__requirements__,
    data_files=[
        ('', ['ReleaseNotes.md']),
    ],
    # For data inside packages can use the automatic inclusion
    # include_package_data = True,
    # or the explicit inclusion, eg:
    # package_data = { 'package_name': ['data.file1', 'data.file2' , ...] }
)