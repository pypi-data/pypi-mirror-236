from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='aws3lib',
  version='1.0.5',
  author='pro0xy',
  author_email='nosammy09@gmail.com',
  description='Library for working with AWS S3 storage',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/prooxyyy/aws3lib',
  packages=['aws3lib'],
  install_requires=['boto3'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='aws3 aws s3 awss3',
  project_urls={
    'Documentation': 'https://github.com/prooxyyy/aws3lib/blob/master/aws3lib/example.py'
  },
  python_requires='>=3.8'
)