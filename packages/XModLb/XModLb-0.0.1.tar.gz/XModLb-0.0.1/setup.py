from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='XModLb',
    version='0.0.1',
    description='This library was created to shorten the process of creating Python scripts.',
    author= 'Rizky Nurahman',
    url = 'https://github.com/XMod-04/XModLb',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=["python", "short"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    py_modules=['XModLb'],
    package_dir={'':'src'},
    install_requires = [
        'requests',
        'beautifulsoup4'
    ]
)