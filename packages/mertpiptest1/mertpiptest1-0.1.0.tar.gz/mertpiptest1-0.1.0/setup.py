import pathlib

import setuptools

setuptools.setup(
    name="mertpiptest1",
    version="0.1.0",
    author="Mert Karlik",
    author_email="mert.karlik@pointr.tech",
    description="A small example package for testing",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://mertpiptest1.pointr.cloud",
    license="The Unlicense",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10, <3.12",
    install_requires=["requests"],
    include_package_data=True,
)
