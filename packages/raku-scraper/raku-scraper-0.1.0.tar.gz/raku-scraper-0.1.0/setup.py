from setuptools import setup, find_packages

setup(
    name="raku-scraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'selenium'
    ],
    author="Petar Yordanov",
    author_email="petaryrdnv@gmail.com",
    description="A simple web scraping and automation tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pyrdnv/raku-scraper",
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
