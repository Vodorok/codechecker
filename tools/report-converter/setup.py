#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="report-converter",
    version="0.1.0",
    author='CodeChecker Team (Ericsson)',
    description="Parse and create HTML files from one or more '.plist' "
                "result files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ericsson/CodeChecker",
    keywords=['report-converter', 'codechecker', 'plist'],
    license='LICENSE.txt',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7"
    ],
    entry_points={
        'console_scripts': [
            'report-converter = codechecker_report_converter.cli:main'
        ]
    },
)
