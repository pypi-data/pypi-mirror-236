from setuptools import setup
from setuptools import setup, find_packages


def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="gs_update_utils",
    version="1.0.4",
    author="xgzx",
    author_email="vadijimory@gmail.com",
    description="Utilities for working with Google Sheets: establishing a connection, reading data from a sheet, and uploading a DataFrame to Google Sheets with retry support.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "gspread",
        "gspread-dataframe",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="example python",
    python_requires=">=3.7",
)
