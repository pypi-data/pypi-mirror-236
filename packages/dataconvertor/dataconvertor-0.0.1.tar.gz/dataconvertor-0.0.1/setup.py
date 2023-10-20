from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='dataconvertor',
  version='0.0.1',
  author='penvoy',
  author_email='zcmll356@gmail.com',
  description='This is the simplest module for quick work with data.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/penvoy/lib_dataconvertor.git',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/penvoy/lib_dataconvertor.git'
  },
  python_requires='>=3.6'
)