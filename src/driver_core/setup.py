from setuptools import setup, find_packages

setup(name='driver_core',
      version='0.1.0',
       packages=find_packages(include=['driver_core', 'driver_core.*'])
      )