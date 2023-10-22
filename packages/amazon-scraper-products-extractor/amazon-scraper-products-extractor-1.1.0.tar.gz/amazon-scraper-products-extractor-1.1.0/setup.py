from setuptools import find_packages
from setuptools import setup

# Package metadata
PACKAGE_NAME = 'amazon-scraper-products-extractor'
VERSION = '1.1.0'
DESCRIPTION = 'A Python library for scraping Amazon product data.'
LONG_DESCRIPTION = '''\
The Amazon Scraper API is a powerful Python library that allows you to scrape product information from Amazon's website. It provides easy-to-use functions to extract product details, prices, reviews, and more. Use it to gather data for market research, price tracking, or any application that requires Amazon product information.

Key Features:
- Retrieve product details, including title, description, and ASIN.
- Get pricing information, including the current price and any discounts.
- Scrape customer reviews, ratings, and review summaries.
- Perform searches and extract search results.

This library is designed to be user-friendly and provides extensive documentation and examples to get you started quickly.
'''
URL = 'https://github.com/yourusername/amazon-scraper-api'
AUTHOR = 'Your Name'
AUTHOR_EMAIL = 'your.email@example.com'
LICENSE = 'MIT'

# Package requirements
REQUIRES = [
    'requests',
    'beautifulsoup4',
]

# Entry points
ENTRY_POINTS = {
    'console_scripts': [
        'amazon-scraper = amazon_scraper_api.cli:main',
    ],
}

# Package classifiers
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=find_packages(),
    install_requires=REQUIRES,
    entry_points=ENTRY_POINTS,
    classifiers=CLASSIFIERS,
)
