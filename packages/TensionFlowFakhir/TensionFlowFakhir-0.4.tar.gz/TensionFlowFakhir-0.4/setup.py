from setuptools import setup, find_packages

setup(
    name="TensionFlowFakhir",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        "numpy",
        "graphviz",
    ],
)
