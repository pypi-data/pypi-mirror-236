import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiosmartoilgauge",
    version="1.0.0",
    author="Dominick Meglio",
    license="MIT",
    author_email="dmeglio@gmail.com",
    description="Provides ability to query the Connected Consumer Smart Oil Gauge REST API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dcmeglio/aiosmartoilgauge",
    packages=setuptools.find_packages(),
    install_requires=["pyjwt", "httpx"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
