from setuptools import setup, find_packages

setup(
    name='simple_wkt',
    version='1.1',
    package_dir={'': 'src'},  # Specify the src directory
    packages=find_packages(where='src'),  # Look for packages in src
    install_requires=[
        'pytest',
        'shapely',
        'pydantic',
    ],
)