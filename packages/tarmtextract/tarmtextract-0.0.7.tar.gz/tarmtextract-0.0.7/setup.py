from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf8") as file:
    # long_description = file.read()

VERSION = '0.0.7'
DESCRIPTION = 'A package that allows to extract text from pdf/word file which is save in aws s3'

# Setting up
setup(
    name="tarmtextract",
    version=VERSION,
    author="Paras Deshbhratar",
    author_email="<paras.d13@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    # long_description=long_description,
    packages=find_packages(),
    install_requires=['pdfplumber', 'textract', 'boto3'],
    keywords=['python', 'textract', 'pdfplumber', 'textextractor'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)