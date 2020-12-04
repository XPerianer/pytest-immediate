#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-immediate',
    version='0.1.0',
    author='Dominik Meier',
    author_email='dominik.meier@student.hpi.de',
    maintainer='Dominik Meier',
    maintainer_email='dominik.meier@student.hpi.de',
    license='MIT',
    url='https://github.com/XPerianer/pytest-immediate',
    description='A plugin helping to get immediate feedback with pytest. Reordering + report of errors using websockets.',
    long_description=read('README.rst'),
    py_modules=['pytest_immediate'],
    python_requires='>=3.5',
    install_requires=['pytest>=6.1.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'immediate = pytest_immediate',
        ],
    },
)
