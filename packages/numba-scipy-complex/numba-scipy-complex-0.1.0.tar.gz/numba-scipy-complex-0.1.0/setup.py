from setuptools import find_packages, setup

with open("package/README.md", "r") as f:
    long_description = f.read()

setup(
    name="numba-scipy-complex",
    version="0.1.0",
    description="Implements a collection of scipy.special functions with support for complex arguments during the"
                "Numba nopython mode.",
    package_dir={"": "package"},
    packages=find_packages(where="package"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoachimMarin/numba-scipy-complex",
    author="Joachim Marin",
    author_email="joachim.marin@t-online.de",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.22.4",
        "scipy>=1.7.3",
        "numba>=0.57.1"
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.9",
)
