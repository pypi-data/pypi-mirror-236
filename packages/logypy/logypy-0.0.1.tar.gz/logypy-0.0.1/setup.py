from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Effortless Python Logging for All Your Projects'
LONG_DESCRIPTION = 'Simplify logging in Python with an easy-to-use package that allows you to create and manage logs seamlessly in your applications. Streamline debugging, error tracking, and activity monitoring with a single function call.'


# Setting up
setup(
    name="logypy",
    version=VERSION,
    author="dev-frog",
    author_email="<kali.nisga@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'logging', 'log', 'logpy', 'logpy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)