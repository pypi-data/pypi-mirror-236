from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Python package for automated feature engineering and machine learning.'
LONG_DESCRIPTION = 'A package to use for automated machine learning using gui or without care about code'

# Setting up
setup(
    name="automlll",
    version=VERSION,
    author="Yash Bravaliya",
    author_email="yashbaravaliya206@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/YashBaravaliya/automll_package",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    INSTALL_REQUIRES = [
    "streamlit",
    "scikit-learn",
    "streamlit_extras",
    "pandas",
    "numpy",
    "plotly",
    "streamlit_option_menu"
    ],
    keywords=['auto ml','no code ml','model'],
    LICENSE = "MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>3.6',
    py_modules=['automlll'],
    package_dir={'':'automll_package'},
    entry_points={
        'console_scripts': [
            'automlll = automlll:main'
        ]
    }
)