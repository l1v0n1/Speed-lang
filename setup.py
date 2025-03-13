from setuptools import setup, find_packages

setup(
    name="speed-lang",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "llvmlite>=0.39.0",
        "rply>=0.7.8",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=0.950",
            "pytest-cov>=3.0.0",
        ],
    },
    author="Speed Language Team",
    author_email="team@speed-lang.org",
    description="A universal programming language combining Python's simplicity with C++'s performance",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/speed-lang/speed",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "speed=speed.__main__:main",
        ],
    },
) 