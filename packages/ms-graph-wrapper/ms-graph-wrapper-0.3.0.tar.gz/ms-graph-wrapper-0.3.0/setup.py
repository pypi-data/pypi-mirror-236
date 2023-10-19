from setuptools import setup, find_packages

setup(
    name="ms-graph-wrapper",
    version="0.3.0",
    author="Sanket Joshi",
    description="A Python wrapper for the Microsoft Graph API that simplifies pagination and provides a more Pythonic interface.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    fullname="ms_graph_wrapper",
    install_requires=["requests","msal","configparser","json"],
)