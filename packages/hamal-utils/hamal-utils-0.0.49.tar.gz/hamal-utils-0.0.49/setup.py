from setuptools import setup, find_packages

setup(
    name='hamal-utils',
    version="0.0.49",
    packages=find_packages(),
    install_requires=[
        'requests',
        'boto3',
        'prefect',
        'numpy',
    ],
    author_email='daniel@cain-technologies.com',
    license='MIT',
)
