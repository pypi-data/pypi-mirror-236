'''
Logging set as datetime directory
'''

from setuptools import setup
from io import open

with open('requirements.txt', encoding="utf-8-sig") as f:
    requirements = f.readlines()

def readme():
    with open('README.md', encoding="utf-8-sig") as f:
        README = f.read()
    return README

setup(
    name='logging_datetime',
    packages=['logging_datetime'],
    include_package_data=True,
    version='1.1.1',
    install_requires=requirements,
    scripts=['logging_datetime/logging_datetime.py'],
    license='Apache License 2.0',
    description='Logging set as datetime directory',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Ali Mustofa',
    author_email='hai.alimustofa@gmail.com',
    url='https://github.com/Alimustoofaa/logging_datetime',
    download_url='https://github.com/Alimustoofaa/logging_datetime.git',
    keywords=['logging', 'log', 'logging directory', 'logging datetime', 'logging datetime directory'],
    classifiers=[
        'Development Status :: 5 - Production/Stable'
    ],
)