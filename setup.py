# Setup script

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