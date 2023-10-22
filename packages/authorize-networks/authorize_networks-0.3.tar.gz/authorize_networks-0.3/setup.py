from setuptools import setup, find_packages

setup(
   name='authorize_networks',
   version='0.3',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      authorize_networks=authorize_networks:cli
      ''',
)