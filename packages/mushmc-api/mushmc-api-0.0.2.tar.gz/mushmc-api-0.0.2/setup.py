from setuptools import setup


with open('README.md', 'r', encoding='utf-8') as fi:
    long_description = fi.read()

setup(
    name='mushmc-api',
    version='0.0.2',
    packages=['mushmc_api'],
    url='https://github.com/Henrique-Coder/mushmc-api',
    author='Henrique-Coder',
    author_email='henriquemoreira10fk@gmail.com',
    description='MushMC-API is a Python library for developers that facilitates access to the MushMC server API, making project creation more efficient and dynamic.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
)
