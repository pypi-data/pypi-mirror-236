from codecs import open
from os import path

from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="klym-telemetry",
    version="0.1.12",
    description="Scaffold library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dummy.readthedocs.io/",
    author="Klym Telemetry",
    author_email="example@email.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent"
    ],
    include_package_data=True,
    packages=find_packages('.', exclude=['tests', 'tests.*']),
    install_requires=[
        'opentelemetry-instrumentation-django~=0.40b0',
        'opentelemetry-instrumentation-fastapi~=0.40b0',
        'opentelemetry-instrumentation-requests~=0.40b0',
        'opentelemetry-instrumentation-sqlalchemy~=0.40b0',
        'opentelemetry-instrumentation-psycopg2~=0.40b0',
        'opentelemetry-instrumentation-celery~=0.40b0',
        'opentelemetry-instrumentation-aiohttp-client~=0.40b0',
        'opentelemetry-exporter-otlp-proto-grpc~=1.19.0',
        'opentelemetry-propagator-aws-xray~=1.0.1',
        'opentelemetry-sdk-extension-aws~=2.0.1'
    ],
    python_requires='>=3.6',
)
