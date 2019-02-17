from setuptools import setup

setup(name='bhavcopy',
      version='0.1',
      description='A simple python script that fetches daily bhav copy data '
                  'from BSE website and serves the data on a webpage',
      url='http://github.com/daltonfury42/bhavcopy',
      author='Dalton Fury',
      author_email='daltonfury42@disroot.org',
      license='MIT',
      packages=['bhavcopy'],
      install_requires=[
          'redis',
          'cherrypy',
           'Jinja2',
      ],
      zip_safe=False)
