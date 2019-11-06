import setuptools
from distutils import sysconfig
site_packages_path = sysconfig.get_python_lib()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyauditlogger",
    version="0.0.1",
    author="path/to/file",
    author_email="path.to.file@gmail.com",
    description="Adds Python Audit hooks to all python scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pathtofile/pyauditlogger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=[("Lib/site-packages", ["zpyauditlogger.pth"])],
    python_requires='>=3.8',
)
