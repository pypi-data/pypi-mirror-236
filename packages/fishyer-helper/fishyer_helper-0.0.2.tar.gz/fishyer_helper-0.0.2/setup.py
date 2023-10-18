from setuptools import setup, find_packages

packages = find_packages()
print(packages)

setup(
    name="fishyer_helper",
    version="0.0.2",
    packages=packages,
    description="My Python Util Package",
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
