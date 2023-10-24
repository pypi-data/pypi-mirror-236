from distutils.core import setup
from setuptools import find_namespace_packages

name = 'datasphere'

setup(
    name=name,
    version='0.5',
    license='Apache-2.0',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
    ],
    tests_require=['pytest', 'pytest-mock'],
    author="Yandex LLC",
    author_email="cloud@support.yandex.ru",
    packages=find_namespace_packages(include=(f'{name}*', 'yandex*', 'google*')),
    package_data={
        name: ['logs/logging.yaml', 'envzy/logs/logging.yml', 'envzy/version/version'],
    },
    install_requires=[
        'grpcio',
        'requests',
        'pyyaml',
        'tabulate>=0.9.0',
        # envzy deps
        'typing-extensions>=4.4.0',
        'appdirs>=1.4.4,<2.0.0',
        'importlib-metadata>=4.8.1',  # TODO drop after dropping 3.9!
        'packaging>=21.3.0',
        'pypi-simple>=1.1.0,<2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'datasphere = datasphere.main:main',
        ],
    },
    python_requires=">=3.8",
    description='Yandex Cloud DataSphere',
    long_description_content_type='text/markdown',
    long_description='Yandex Cloud DataSphere',
)
