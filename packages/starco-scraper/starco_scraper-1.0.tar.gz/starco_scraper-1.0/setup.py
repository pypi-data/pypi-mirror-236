from setuptools import setup

requires = [
    'beautifulsoup4==4.12.2',
    'lxml==4.9.3',
    'requests==2.31.0',
]
setup(
    name = 'starco_scraper',
    version='1.0',
    author='Mojtaba Tahmasbi',
    packages=['scraper'],
    install_requires=requires,
)