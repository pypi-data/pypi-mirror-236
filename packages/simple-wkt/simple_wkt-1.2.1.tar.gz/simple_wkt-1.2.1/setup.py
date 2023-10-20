from setuptools import setup, find_packages

VERSION = '1.2.1'
DESCRIPTION = 'A package for basic interaction with WKT objects'

# Setting up
setup(
    name="simple_wkt",
    version=VERSION,
    author="",
    author_email="",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pydantic', 'shapely'],
)
