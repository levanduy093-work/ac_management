#!/usr/bin/env python3
"""
Setup script for PZEM-004T Power Monitoring Library
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pzem004t",
    version="2.0.0",
    author="AC Management Team",
    author_email="support@acmanagement.com",
    description="A comprehensive Python library for the PZEM-004T AC Power and Energy meter",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ac_management",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: System :: Hardware",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "pzem-monitor=tools.read_ac_sensor:main",
            "pzem-reset=tools.reset_energy:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 