from setuptools import setup, find_packages
import os,sys

main_ns = dict()
with open(f"{os.path.abspath(os.path.dirname(__file__))}\\src\\optboolnet\\version.py") as ver_file:
    exec(ver_file.read(), main_ns)
    VERSION = main_ns["__version__"]

# TODO: include dependencies: pao, pyutilib
setup(
    name="optboolnet",
    version=VERSION,
    description="The optimization toolbox for control problems of a Boolean network",
    long_description=open('README.md').read(),
    url="https://www.msolab.org/",
    author="MSO Lab",
    author_email="mso.postech@gmail.com",
    license_files=("LICENSE.txt"),
    install_requires=["boolean.py", "colomoto_jupyter", "pyomo", "gurobipy"],
    entry_points={
        "console_scripts": [],
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    zip_safe=False,
)
