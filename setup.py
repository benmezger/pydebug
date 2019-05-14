from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python-pydebug",
    version="0.2",
    description="A set of debugging decorators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/benmezger/pydebug",
    author="Ben Mezger",
    author_email="me@benmezger.nl",
    license="MIT",
    packages=["pydebug"],
    zip_safe=False,
)
