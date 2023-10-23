# -*- coding: utf-8 -*-
"""Setup file.

Reminder for PyPI uploading (currently manual).
 - Install twine if don't have it
 - python setup.py sdist bdist_wheel
 - Test with PyPI until it looks good, but note you can't install from there
   because it's missing dependencies
     twine upload -r testpypi dist/* -u jennirinker -p PASSWORD
 - Once it is greenlighted, upload to PyPI
     twine upload dist/* -u jennirinker -p PASSWORD
 - Tag the branch with the corresponding version
"""
from os import path
from setuptools import setup, find_packages

d_path = "test/_data/"


def load_readme():
    """Load readme to put into pypi long description"""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setup(name='lacbox',
      version='0.0.7',
      description='Toolbox for LAC course at DTU Wind Energy',
      long_description=load_readme(),
      long_description_content_type='text/markdown',
      url='https://gitlab.windenergy.dtu.dk/lac-course/dtulac',
      author='DTU Wind Energy',
      author_email='rink@dtu.dk',
      license='MIT',
      packages=find_packages(),
      package_data={"": 
        [d_path+ext for ext in ["*.ind", "*.pwr", "*.hdf5", "*.dat", "*.cmb", "*.amp"]]
        +
        [d_path+"dtu_10_mw/*", d_path+"dtu_10_mw/data/*"]
      },
      install_requires=['h5py',  # for gtsdf loading
                        'jupyter',  # run demos
                        'matplotlib',  # plotting
                        'numpy',  # numberic arrays
                        'pandas',  # for gtsdf handling and post-processing
                        'scipy',  # Interpolation
                        'tables',  # saving/loading stats files in hdf5 format
                        ],
      zip_safe=False)
