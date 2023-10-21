from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="wrapper_kafka",
    version="0.0.3",
    description="Wrapper around python-kafka with pydantic serialization"
                " and prometheus-client monitoring for easy prod implementation",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Pavel Tiurin",
    author_email="pavel.tyurin@veeam.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["kafka-python==2.0.2", "prometheus-client==0.17.1", "pydantic==2.4.2"],
    python_requires=">=3.8"
)
