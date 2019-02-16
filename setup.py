from setuptools import setup

setup(name='bhavcopy',
      version='0.1',
      description='A simple python script that fetches daily Bhav Copy data from BSE website and serves the data on a website',
      url='http://github.com/daltonfury42/bhavcopy',
      author='Dalton Fury',
      author_email='daltonfury42@disroot.org',
      license='MIT',
      packages=['bhavcopy'],
      install_requires=[
          'redis'
      ],
      zip_safe=False)
