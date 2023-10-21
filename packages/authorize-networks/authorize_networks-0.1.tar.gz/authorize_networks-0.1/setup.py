from setuptools import setup, find_packages

setup(
   name='authorize_networks',
   version='0.1',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      authorize_networks=authorize_networks_main:cli
      ''',
)