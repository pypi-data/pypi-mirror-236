from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Anomaly detection for one-dimensional data'

setup(
    name="xiezhi-ai",
    author="Zhilin Wang",
    author_email="wang5327@purdue.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md',encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'anomaly detection', 'one-dimentional data'],
    license="MIT",
)