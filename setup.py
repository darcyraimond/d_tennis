import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="d_tennis",
    version="0.0.1",
    author="Darcy Raimond",
    author_email="darcy.raimond@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",

    #package_dir={"": "src"},
    packages=["src"],#setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)


"""project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },"""
"""classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],"""