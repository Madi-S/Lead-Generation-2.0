from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

VERSION = '0.2.0'
DESCRIPTION = 'Lead generation scripts'

setup(
    name='lead-generation',
    version=VERSION,
    author='Madi-S (Madi Shaiken)',
    author_email='<khovansky99@gmail.com>',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['playwright', 'beautifulsoup4', 'geopy'],
    keywords=['python', 'lead generation', 'web automation',
              'playwright', 'google maps', 'yelp'],
    classifiers=[
        'Development Status :: 3 - Released/In progress',
        'Intended Audience :: Developers, Managers, Lead Generators',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)
