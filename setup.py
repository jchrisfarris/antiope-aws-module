from setuptools import setup, find_packages
import os, sys

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name='antiope',
  version=os.popen('{} antiope/_version.py'.format(sys.executable)).read().rstrip(),
  author='Chris Farris',
  author_email='chris@room17.com',
  license="Apache License 2.0",
  license_file="LICENSE",
  description='Library for interacting with AWS accounts that are tied to the Antiope framework',
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=find_packages(),
  py_modules=['antiope'],
  url='https://github.com/WarnerMedia/antiope-aws-module.git',
  python_requires='>=3.6',
  include_package_data=True,
  install_requires=[
    'boto3 >= 1.10.0',
    'botocore >= 1.13.0'
  ]
)
