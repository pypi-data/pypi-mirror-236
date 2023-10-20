from setuptools import setup, find_packages

setup(
    name='univ360',
    version='0.1.2',
    author='Anton Zhidkov, Vlad Bespalov',
    packages=['univ360'],
    description='Module for v360 files',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.10',
    install_requires=[
        'urllib3',
        'Pillow',
        'base64',
        'glob',
        'io',
        'json',
        'dataclasses',
        'os',
        're'
    ],
)