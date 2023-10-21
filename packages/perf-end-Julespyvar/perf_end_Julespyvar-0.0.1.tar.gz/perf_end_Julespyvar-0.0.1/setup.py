from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="perf_end_Julespyvar",
    version="0.0.1",
    author="Bohus Gyula",
    author_email="gyuszkob@gmail.com",
    description="prediction models for athletes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/perfendpred_packaging",  # No repo yet
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7,<4",
    install_requires=[
        "keras==2.8.0",
        "numpy==1.22.2",
        "scikit-learn==1.1.3",
        "tensorflow==2.8.0",
        "joblib==1.3.2",
        "setuptools==57.4.0"
    ],
    include_package_data=True  
)
