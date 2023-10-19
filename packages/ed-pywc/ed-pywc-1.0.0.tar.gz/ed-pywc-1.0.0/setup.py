from setuptools import find_packages, setup

setup(
    name="ed-pywc",
    version="1.0.0",
    description="Python implementation of the UNIX wc (Word Count) utility",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ed Chapman",
    author_email="ed@edchapman.co.uk",
    url="https://github.com/edjchapman/pywc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="cli tool wc word count",
    install_requires=[
        "click>=8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "flake8>=6.0",
            "isort>=5.12",
        ],
    },
    entry_points={
        "console_scripts": [
            "pywc=pywc.main:wc",
        ],
    },
    python_requires=">=3.6",
)
