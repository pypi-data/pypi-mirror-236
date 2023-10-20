from setuptools import setup, find_packages

setup(
    name="acsefunctions",
    version="0.5",
    packages=find_packages(),
    

    author="Manawi Kahie",
    author_email="mk1923@ic.ac.uk",
    description="Computes acsefunctions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/acse-mk1923/acsefunctions",
    

    install_requires=[

    ],


    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

