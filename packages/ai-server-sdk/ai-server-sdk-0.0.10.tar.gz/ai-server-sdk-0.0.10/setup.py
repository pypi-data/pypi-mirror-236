from setuptools import find_packages, setup

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name="ai-server-sdk",                     # This is the name of the package
    version="0.0.10",
    packages=find_packages(),
    install_requires=['requests',], 
    author="Thomas Trankle",                     # Full name of the author
    description="Utility package to connect to AI Server instances.",
    license="MIT",
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)