import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rmwrapper",
    version="0.0.1",
    author="ad044",
    author_email="",
    description="Minimal wrapper for Redditmetrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d9x33/rmwrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
