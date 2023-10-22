import setuptools
from pathlib import Path

setuptools.setup(
    name="totpak",
    version="1.0.3",
    long_description=Path("README.md").read_text(),
    # packages=setuptools.find_packages(exclude=["tests", "data"])
    packages=["totpak"]  # the line above didn't seem to work
)
