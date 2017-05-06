import os
import sys
import os.path as op
from setuptools import setup, find_packages

name = 'BCItp'
files = [name, ]

root = op.dirname(op.abspath(__file__)) + op.sep

# remove all *.pyc files here before packaging
if 'sdist' in sys.argv:
    rem_files = []
    for path, folders, filenames in os.walk(root):
        for file in filenames:
            rem_files.append(op.join(path, file))
    for file in rem_files:
        if '.pyc' in file:
            print('Removing {}'.format(file))
            os.remove(file)

setup(
    name=name,
    packages=find_packages(),
    include_package_data=True,
    install_requires=['kivy', 'numpy', 'scipy', 'matplotlib'],
    # version=version,
    description='BCItp - Brain Computer Interface training platform',
    author='Rafael Duarte',
    author_email='rmendesduarte@gmail.com',
    url='https://github.com/rafaelmendes/BCItp',
    keywords=['bcitp', 'bci', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
)
