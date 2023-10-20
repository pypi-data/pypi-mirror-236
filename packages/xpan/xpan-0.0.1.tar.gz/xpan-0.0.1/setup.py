import codecs
import os

from setuptools import find_packages, setup

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '0.0.1'
DESCRIPTION = 'An API library for BaiduNetdisk'
LONG_DESCRIPTION = 'An API library for BaiduNetdisk'

# Setting up
setup(
    name="xpan",
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "urllib3 >= 1.25.3",
        "python-dateutil"
    ],
    keywords=['BaiduNetdisk','openapi_client'],
    python_requires='>=3.6',
)