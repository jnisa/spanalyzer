from setuptools import setup, find_packages

setup(
    name="spanalyzer",
    version="1.0.4",
    packages=find_packages(),
    install_requires=[
        "javalang",
    ],
    entry_points={
        'console_scripts': [
            'spanalyzer=spanalyzer.cli:main',
        ],
    },
    description="OpenTelemetry Code Analysis Tool",
    author="Joao Nisa",
    author_email="joao.je.nisa@gmail.com",
    url="https://github.com/jnisa/spanalyzer",
    python_requires=">=3.10",
)

