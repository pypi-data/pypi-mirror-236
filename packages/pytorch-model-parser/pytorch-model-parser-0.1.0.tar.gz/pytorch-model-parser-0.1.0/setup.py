from setuptools import setup, find_packages

setup(
    name="pytorch-model-parser",
    version="0.1.0",
    description="A library to parse PyTorch CNN models and retrieve layer details.",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
