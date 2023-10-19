from setuptools import setup, find_packages

setup(
    name="MS Graph Wrapper",
    version="0.1.0",
    description="A wrapper for the Microsoft Graph API to make it easier to use in Python.You don't need to write the pagination code, the wrapper will do it for you.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)