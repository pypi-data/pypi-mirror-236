from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="nlpstreamline",
    version="0.0.10",
    description="Streamline basic text & NLP processing",
    package_dir={"": "nlpstreamline"},
    packages=find_packages(where="nlpstreamline"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CielZ001/NLPStreamline",
    author="XiZhao",
    author_email="cielxxzhao@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=["nltk"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.8",
)