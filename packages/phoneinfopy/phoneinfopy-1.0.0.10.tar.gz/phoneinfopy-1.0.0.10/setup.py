from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0.0.10'
DESCRIPTION = "phoneinfopy is a Python package that allow you to get respones from truecaller APIs. You can able to do login, OTP verification, and phone number search using Truecaller API with this package."

# Setting up
setup(
    name="phoneinfopy",
    version=VERSION,
    author="Mr_3rr0r_501 [yuvaraj]",
    author_email="<yuvarajucet@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['truecaller','phoneinfo', 'numberinfo', 'phonenumberinfo'],
	classifiers = [
	    "Topic :: Utilities",
	    "Natural Language :: English",
	    "Operating System :: OS Independent",
	    "Programming Language :: Python :: 3",
	]
)
