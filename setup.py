#from distutils.core import setup
from setuptools import setup

setup(
    name='GrobnerSolver',
    description='Computer Algebra solver for Groebner basis',
    version='0.1',
    author='Rex McArthur',
    author_email='drexmcarthur@gmail.com',
    packages=['GrobnerSolver'],
    license='MIT',
    classifiers=['Development Status :: 3 -Alpha', 
                'Programming Language :: Python :: 2.7'],

    long_description=open('README').read(),
    url='https://github.com/drexmca/GrobnerSolver',
)



