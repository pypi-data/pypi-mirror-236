import os
from setuptools import setup, find_packages
from importlib.machinery import SourceFileLoader

version = (
    SourceFileLoader("protectremote.version", os.path.join("protectremote", "version.py")).load_module().VERSION
)

setup(
    name='protectremote',
    version=version,
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Next-gen security solution for remote workers',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    install_requires=['python-settings',"flask", "apscheduler", "python-dotenv"],
    author='Protect Remote',
    author_email='sinan.bozkus@gmail.com',
    keywords=['security'],
    include_package_data=True,
     package_data = {
        '': ['*.html', '*.css'],
    },
)