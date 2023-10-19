from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='infotest',
  version='0.1.1',
  author='Eugene Bez',
  author_email='holodische@gmail.com',
  description='This is a test module to demonstrate the creation of libraries.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Holodische/LibTest',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files infotest',
  project_urls={
    'GitHub': 'https://github.com/Holodische/LibTest'
  },
  python_requires='>=3.10'
)