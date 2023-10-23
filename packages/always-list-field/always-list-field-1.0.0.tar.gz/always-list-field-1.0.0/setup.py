from setuptools import setup, find_packages

setup(
    name="marshmallow-always-list",
    version="0.1.0",
    description="This is a small package that will ensure that your marshmallow will alway contain list",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Dominik Szymanski",
    author_email="dominosz89@gmail.com",
    url="https://github.com/szymansd/marshmallow-always-list-field",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "marshmallow==3.14.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)
