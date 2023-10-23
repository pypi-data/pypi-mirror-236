import setuptools
from pathlib import Path

setuptools.setup(
    name="dayapdf",
    version="1.0",
    # Use read_bytes() to read as bytes
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
