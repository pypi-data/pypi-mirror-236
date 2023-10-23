from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + "".join(fh.readlines()[3:])

VERSION = "0.3.0"
DESCRIPTION = "Package with utility functions and classes to work with Pygame."

setup(
    name="pygutils",
    version=VERSION,
    license="MIT",
    author="Lucas Eliaquim",
    author_email="<lemsantos.dev@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["pygame"],
    tests_require=["parameterized"],
    keywords=["python", "pygame", "utility", "helpers"],
    project_urls={
        "Bug Tracker": "https://github.com/LEMSantos/pygutils/issues",
        "Source": "https://github.com/LEMSantos/pygutils",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10",
)
