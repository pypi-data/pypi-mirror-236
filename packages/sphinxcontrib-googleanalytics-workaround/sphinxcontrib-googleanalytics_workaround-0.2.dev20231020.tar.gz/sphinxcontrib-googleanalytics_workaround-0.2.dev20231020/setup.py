# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, 'README.rst')) as f:
    long_desc = f.read()

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-googleanalytics_workaround',
    version='0.2',
    url='https://github.com/sphinx-contrib/googleanalytics',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-googleanalytics',
    license='BSD',
    author='Domen Kozar',
    author_email='domen@dev.si',
    description='Sphinx extension googleanalytics',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
