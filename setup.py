import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modulemap",
    version="0.0.1",
    author="Sam Ingram",
    author_email="sp_ingram12@yahoo.co.uk",
    description="A lightweight option for creating json description files of Python modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/singram12/ModuleMap",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
   'jsondiff>=1.2.0',
    ],
    python_requires='>=3.5',
)