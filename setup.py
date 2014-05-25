#!/usr/bin/python
# -*- coding: utf8 -*-
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='django-rest-forum',
    version='0.1.1',
    author='Mo Mughrabi',
    author_email='mo.mughrabi@gmail.com',
    url='https://github.com/',
    description='Web pages capture using Django & CasperJS',
    long_description=open(os.path.join(here, 'README.rst')).read() + '\n\n' + 
                     open(os.path.join(here, 'CHANGES')).read(),
    license='LPGL, see LICENSE file.',
    install_requires = ['Django'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers  = ['Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Environment :: Web Environment',
                    'Framework :: Django',
                    'Programming Language :: Python :: 2.7'],
)
