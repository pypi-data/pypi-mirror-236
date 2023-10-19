from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='At1set_library',
  version='0.0.04',
  author='At1set',
  author_email='iliya9874329@gmail.com',
  description='This is my first test library',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='',
  packages=find_packages(),
  # install_requires=['requests>=2.25.1'],
  install_requires=['PyAutoGUI'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='',
  project_urls={
    'GitHub': 'https://github.com/At1set'
  },
  python_requires='>=3.6'
)