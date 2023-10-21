import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybab",
    version="0.0.1",
    author="Abdelouahed Ben Mhamed",
    install_requires=["numpy"],
    license="MIT",
    author_email="a.benmhamed@intelligentica.net",
    description="PyBaB: A Python Library for solving mixed-integer linear models using enhanced branch-and-bound with bayesian inference    .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmedfgad/GeneticAlgorithmPython",
    packages=setuptools.find_packages())