from setuptools import setup

VERSION = '0.0.10'
DESCRIPTION = 'Allow to create restartable lambda'
LONG_DESCRIPTION = 'A base class containing useful methods to monitor and restart a lambda while keeping its context, storing it on AWS'

# Setting up
setup(
  name="restartable_lambda",
  version=VERSION,
  author="Samuel Courthial",
  author_email="samuel.courthial.18@gmail.com",
  description=DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  packages=['restartable_lambda'],
  install_requires=[
    'boto3==1.23.10',
    'retrying==1.3.3'
  ],
  keywords=['python', 'aws', 'lambda', 'restartable', 'restart', 'boto3'],
  classifiers= [
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3"
  ]
)