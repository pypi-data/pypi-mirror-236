from setuptools import setup, find_packages

VERSION = '0.0.13'
DESCRIPTION = 'Make a simple Python OS'
LONG_DESCRIPTION = (
    "This is a Python package for creating a simple operating system. "
    "It provides a basic framework for building an OS in Python."
)

# Setting up
setup(
    name="os_dev",
    version=VERSION,
    author="Bodie Sevcik",
    author_email="bodei11007@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'os', 'operating', 'operating system', 'system', 'easy'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
