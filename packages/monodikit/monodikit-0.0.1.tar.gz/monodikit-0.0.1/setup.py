from setuptools import find_packages, setup

with open("app/Readme.md", "r") as f:
    long_description = f.read()

setup(
    name="monodikit",
    version="0.0.1",
    description="",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timeipert/MonodiKit",
    author="Tim Eipert & Fabian C. Moss",
    author_email="tim.eipert@uni-wuerzburg.de",
    license="",
    classifiers=[""],
    install_requires=[],
    extra_require={
        "dev": ["twine>=4.0.2"]
    },
    python_requires=">=3.8",
)
