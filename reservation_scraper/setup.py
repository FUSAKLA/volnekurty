from setuptools import setup, find_packages

setup(
    name         = 'volnekurty_reservation_scraper',
    version      = '1.0.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = reservation_scraper.settings']},
)
