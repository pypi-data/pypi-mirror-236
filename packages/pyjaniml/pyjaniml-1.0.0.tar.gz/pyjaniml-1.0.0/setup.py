import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pyjaniml",
    version="1.0.0",
    description="Classes for AniML handling",
    author="CLADE GmbH",
    author_email="info@clade.io",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://gitlab.com/clade-gmbh/pyjaniml",
    keywords=["AniML", "json"],
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=["marshmallow>=3.0"],
    extras_require={
        "opus": ["brukeropusreader>=1.3.4"],
    },
    setup_requires=["setuptools_scm>=5"],
    use_scm_version=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
