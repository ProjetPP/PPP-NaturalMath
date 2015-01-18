#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='ppp_natural_math',
    version='0.1',
    description='Natural language processing for math questions for the Projet Pensées\nProfondes.',
    url='https://github.com/ProjetPP',
    author='Valentin Lorentz',
    author_email='valentin.lorentz+ppp@ens-lyon.org',
    license='MIT',
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Development Status :: 1 - Planning',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'ply',
        'ppp_datamodel>=0.6',
        'ppp_libmodule>=0.7',
    ],
    packages=[
        'ppp_natural_math',
    ],
)
