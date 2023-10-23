from setuptools import setup, find_packages

VERSION = '0.0.14'
DESCRIPTION = 'Gives you tools to make an OS in Python'
LONG_DESCRIPTION = 'You can get development tools for an OS in Python!'

# Setting up
setup(
    name="os_dev",
    version=VERSION,
    author="Bodie Sevcik",
    author_email="bodei11007@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,  # Use the correct variable name
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'py', 'os', 'dev', 'system', 'operating'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
