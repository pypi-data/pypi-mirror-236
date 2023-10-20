from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "isqmap",
    version = "0.4",
    keyword = {"mapping", "ustc"},
    description = "a qubit mapping package",
    platforms='python 3.7+',
    long_description=long_description,
	long_description_content_type="text/markdown",
    author = "arclightquantum",
    author_email = "louhz@arclightquantum.com",

    package_data = {'':['*.txt']},
    install_requires = ['numpy',
                        'networkx',
                        'matplotlib',
                        'qiskit'],
    packages = find_packages(),
    zip_safe=False
)
