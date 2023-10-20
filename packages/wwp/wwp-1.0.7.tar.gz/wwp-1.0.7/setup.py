from setuptools import setup, find_packages

setup(
    name='wwp',
    version='1.0.7',
    description='Python module for working with prime numbers',
    author='Munashe',
    author_email='munashemukweya2022@gmail.com',
    url='https://github.com/Langton49/workingWithPrimes',
    keywords='Prime numbers',
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.8.0',
        'numpy>=1.26.0',
    ],
    license="MIT",
)
