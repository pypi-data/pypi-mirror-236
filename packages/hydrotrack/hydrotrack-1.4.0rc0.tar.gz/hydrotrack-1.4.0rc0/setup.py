import os
from ast import parse
import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open(os.path.join('hydrotrack', '_version.py')) as f:
    __version__ = parse(next(filter(lambda line: line.startswith('__version__'),
                                     f))).body[0].value.s

setuptools.setup(
    name="hydrotrack",
    version=__version__,
    author="Helvecio B. L. Neto, Alan J. P. Calheiros",
    author_email="hydrotrack.project@gmail.com",
    description="A Python package for track and forecasting.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/hydrotrack-project/hydrotrack",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    license="LICENSE",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Hydrology",
    ]
)
