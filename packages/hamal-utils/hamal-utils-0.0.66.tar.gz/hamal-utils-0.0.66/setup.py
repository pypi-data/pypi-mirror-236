from setuptools import setup, find_packages
from hamal_utils.code.tools import __VERSION__

setup(
    name='hamal-utils',
    version=__VERSION__,
    packages=find_packages(),
    install_requires=[
        'requests',
        'boto3',
        'prefect',
        'numpy',
        'gitversion',
    ],
    author_email='daniel@cain-technologies.com',
    license='MIT',
)
