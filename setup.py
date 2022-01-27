import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="d_tennis",
    author="Darcy Raimond",
    author_email="darcy.raimond@gmail.com",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=["termcolor"]
)


"""project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },"""
"""classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],"""