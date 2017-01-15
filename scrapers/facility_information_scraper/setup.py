from setuptools import setup, find_packages

setup(
    name         = 'volnekurty_facility_information_scraper',
    version      = '1.0.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = facility_information_scraper.settings']},
)
