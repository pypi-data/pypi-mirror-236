from setuptools import setup
import  codecs
import os
# Define your library's metadata
name = "pylibr"  # Replace with your library name
version = "0.0.2"  # Replace with your library version
description = "this is library "
long_description = "A longer description of your library"




# Create the setup configuration
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author="nick",
    author_email="nick@gmail.com",
    
    install_requires=[],
    classifiers=[
       "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
