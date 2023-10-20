from setuptools import setup, find_packages

setup(
    name='univ360',
    version='0.1.1',
    author='Anton Zhidkov, Vlad Bespalov',
    packages=find_packages(),
    description='Module for v360 files',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.10',
    install_requires=[
        'urllib3',
        'Pillow'
    ],
)