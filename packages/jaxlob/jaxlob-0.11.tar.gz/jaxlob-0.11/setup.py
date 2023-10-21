from setuptools import setup, find_packages

# Read the content of README.md into long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='jaxlob',
    version='0.11',
    packages=find_packages(),
    install_requires=[
        # list your project dependencies here
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)

