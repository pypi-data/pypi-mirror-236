from setuptools import setup

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="d2y",
    version="0.0.11",
    description="A Python SDK for the D2Y Exchange API",
    long_description=long_description,  # Add this line
    long_description_content_type="text/markdown",  # Add this line
    author="d2y Core Team",
    author_email="admin@d2y.exchange",
    url="",
    packages=["d2y"],
    install_requires=["requests", "web3"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
)
