from setuptools import setup, find_packages

setup(
    name='uno-ai',
    version='1.0',
    author='Edward Baker',
    description='A package for playing UNO or to interface with an AI',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
