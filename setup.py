# Setup script

from setuptools import setup
from setuptools import find_packages


install_requires = [
    "javalang",
    "setuptools",
    "python-dotenv",
]

setup(
    name="spanalyzer",
    version="1.0.2",
    description="A tool to analyze telemetry implementation in codebases",
    author="Joao Nisa",
    author_email="joao.je.nisa@gmail.com",
    packages=find_packages(),
    install_requires=install_requires,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["spanalyzer = spanalyzer.cli:main"],
    },
)
