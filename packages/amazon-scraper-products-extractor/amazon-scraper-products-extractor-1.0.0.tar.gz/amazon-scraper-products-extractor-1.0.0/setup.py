from setuptools import find_packages
from setuptools import setup

setup(
    name='amazon-scraper-products-extractor',
    version='1.0.0',
    description='A Python package for scraping product data from Amazon.',
    author='Your Name',
    author_email='your@email.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)
