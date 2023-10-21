from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='libAll',
  version='3.1',
  author='ForestBu',
  author_email='tvc55.admn@gmail.com',
  description='All libraries of PyPi',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/ForestBu/libAll',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='libAll liball alllibraries allibraries perimeter square area python file os system pause time timer login password register log reg',
  python_requires='>=3.7'
)
