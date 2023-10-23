from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='geotriangulate',
  version='1.0.0',
  author='my_nickname',
  author_email='example@gmail.com',
  description='geotriangulate',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/hashdrd/geotriangulate',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='',
  project_urls={
    'Documentation': 'https://github.com/hashdrd/geotriangulate'
  },
  python_requires='>=3.7'
)