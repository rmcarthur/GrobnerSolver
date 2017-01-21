from distutils.core import setup
try:
    long_descrip = open('README.txt').read()
setup(
    name='GroebnerSolver',
    description='Computer Algebra solver for Groebner basis'
    version='0.1',
    author='Rex McArthur',
    author_email='drexmcarthur@gmail.com',
    packages=['GroebnerSolver'],
    scripts=['bin/seansUtils-test', 'bin/research-dnn'],
    license='MIT',
    classifiers=['Development Status :: 3 -Alpha', 
                'Programming Language :: Python :: 2.7'],

    long_description=open('README.txt').read(),
)



