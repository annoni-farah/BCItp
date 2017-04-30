from distutils.core import setup

setup(
    name='BCItp',
    version='0.0.1',
    packages=['bcitp', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    setup_requires=['setuptools>=18.0', 'cython'],
)
