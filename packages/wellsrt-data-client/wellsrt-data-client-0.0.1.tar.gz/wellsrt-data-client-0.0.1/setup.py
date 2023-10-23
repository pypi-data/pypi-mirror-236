# coding: utf-8

"""
    Wells Data Client
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "wellsrt-data-client"
VERSION = "0.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3", "requests", "pyyaml", "python-decouple", "certifi", "python-dateutil", "StrEnum"]

setup(
    name=NAME,
    version=VERSION,
    description="WellsRT Data Client Library",
    author_email="",
    url="",
    keywords=["WellsRT Data Client"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    WellsRT Data Client Library  # noqa: E501
    """
)
