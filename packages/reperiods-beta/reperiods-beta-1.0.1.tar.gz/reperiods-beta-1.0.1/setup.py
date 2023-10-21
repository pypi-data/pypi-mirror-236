import os
from setuptools import find_packages, setup

# get __version__ from _version.py
ver_file = os.path.join("reperiods", "_version.py")
with open(ver_file) as f:
    exec(f.read())

DISTNAME = "reperiods-beta"
DESCRIPTION = "A set of tools to find Representative Periods."
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()
URL = ""
LICENSE = ""
DOWNLOAD_URL = ""
VERSION = __version__  # noqa
INSTALL_REQUIRES = ["pandas>=2.0.3", "PuLP>=2.7.0", "plotly>=5.15.0","scikit-learn-extra>=0.3.0","numpy>=1.25.2","nbformat>=4.2.0"]
CLASSIFIERS = [
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
]
EXTRAS_REQUIRE = {
    "tests": ["pytest", "pytest-cov","twine","wheel"],
    "docs": [
        "pillow",
        "sphinx",
        "sphinx-gallery",
        "sphinx_rtd_theme",
        "numpydoc",
        "matplotlib",
    ],
}



setup(
    name=DISTNAME,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.10",
)