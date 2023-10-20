from setuptools import setup, find_packages

setup(
    name='univ360',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'urllib3',
        'Pillow'
    ],
)