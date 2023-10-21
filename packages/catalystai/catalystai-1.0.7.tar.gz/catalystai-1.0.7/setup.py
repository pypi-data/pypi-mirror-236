from setuptools import setup, find_packages

classifiers = [
"Development Status :: 2 - Pre-Alpha",
"Intended Audience :: Education",
"Operating System :: MacOS :: MacOS X",
"Operating System :: Microsoft :: Windows",
"Programming Language :: Python :: 3",
]
setup(
name="catalystai",
version="1.0.7",
description="Catalyst AI SDK",
long_description="CatalystAI SDK allows user to get list of all files in a specific workspace and project. CatalystAI SDK allows user to upload the data to Catalyst Storage for a specific workspace and project. Prerequisite:User should be an active user of Catalyst AI with a valid API key",
url="",
author="Catalyst AI",
author_email="contact@catalystai.com",
license="Catalyst AI",
classifiers=classifiers,
keywords=['python', 'first package'],
packages=find_packages(),
install_requires=[], # add any additional packages that needs to be installed along with your package. 
)