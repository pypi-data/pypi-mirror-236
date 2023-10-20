# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()
  
  
  
setup(name='qtML',  # 包名
      version='1.0.0',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='richotech',
      author_email='admin@richo-tech.com',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Topic :: Software Development :: Libraries'
      ],
      )