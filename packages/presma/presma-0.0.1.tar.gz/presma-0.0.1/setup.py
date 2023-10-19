from setuptools import setup, find_packages

setup(
    name="presma",
    version="0.0.1",
    url="https://github.com/AkshayJ0shi/demo-cli",
    description="This is short description",
    long_description="This is long description",
    author="AkshayJ",
    author_email="my@email.com",
    install_requires=[
        "setuptools>=56.0.0"
    ],
    packages=find_packages(),
    keywords=["Python", "trial"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)