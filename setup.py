# setup.py
from setuptools import setup, find_packages

setup(
    name="temporal",
    version="0.1.0",
    author="Chris Mangum",
    author_email="csmangum@gmail.com",
    description="A custom python object for storing and managing states in a temporal sequence.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/temporal/",
    packages=find_packages(),
    install_requires=[
        "ipycytoscape",
        "hypothesis",
        "pytest",
        "pyperf",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
