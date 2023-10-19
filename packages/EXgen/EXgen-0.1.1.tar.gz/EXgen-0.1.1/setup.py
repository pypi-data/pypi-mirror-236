#!/usr/bin/env python

from distutils.core import setup

setup(
    name="EXgen",
    version="0.1.1",
    description="Exercise and Exam generating library for electrical engineering.",
    author="Eniz Museljic",
    author_email="emuseljic@tugraz.at",
    url="https://www.tugraz.at/institute/igte/home/",
    packages=["EXgen", "EXgen.util"],
    include_package_data=True,
    scripts=["bin/generate-ex"],
    keywords=["generate", "exam", "exercise", "latex"],
    install_requires=["pyyaml==6.0", 
                      "lcapy==1.7", 
                      "sympy==1.11.1", 
                      "tqdm==4.66.1", 
                      "numpy==1.26.0", 
                      "ypstruct"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    )
