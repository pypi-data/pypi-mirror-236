from setuptools import setup, find_packages

setup(
    name='simple_wkt',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'shapely',
        'pydantic',
    ],
)
