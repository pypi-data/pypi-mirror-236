from setuptools import setup, find_packages

setup(
    name="fishyer-package",
    version="0.2",
    packages=find_packages(),
    description="A sample Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="fishyer",
    author_email="yutianran66@gamil.com",
    url="https://github.com/fishyer/python-util",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
