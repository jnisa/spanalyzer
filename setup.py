# Setup script

from setuptools import setup
from setuptools import find_packages

entry_points={
    "flake8.extension": [
        "OTEL = flake8_otel:Flake8OTELAudit",
    ],
},

install_requires=[
    'flake8',
    'ast',
    'pytest',
]

setup(
    name="spanalyzer",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'spanalyzer = spanalyzer.cli:main'
        ],
    },
)