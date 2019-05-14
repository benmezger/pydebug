from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = ["Cython>=0.29.7", "ipdb>=0.12"]

setup(
    name="python-pydebug",
    version="0.3",
    description="A set of debugging decorators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/benmezger/pydebug",
    author="Ben Mezger",
    author_email="me@benmezger.nl",
    license="MIT",
    packages=["pydebug"],
    install_requires=requires,
    zip_safe=False,
    python_requires=">=3.*.*",
    extras_require={"line_profiling": ["line_profiler>=2.1.1"]},
)
