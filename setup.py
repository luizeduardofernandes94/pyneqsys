#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from distutils.core import setup


pkg_name = 'pyneqsys'

PYNEQSYS_RELEASE_VERSION = os.environ.get('PYNEQSYS_RELEASE_VERSION', '')

# http://conda.pydata.org/docs/build.html#environment-variables-set-during-the-build-process
if os.environ.get('CONDA_BUILD', '0') == '1':
    try:
        PYNEQSYS_RELEASE_VERSION = 'v' + open(
            '__conda_version__.txt', 'rt').readline().rstrip()
    except IOError:
        pass

release_py_path = os.path.join(pkg_name, '_release.py')

if (len(PYNEQSYS_RELEASE_VERSION) > 1 and
   PYNEQSYS_RELEASE_VERSION[0] == 'v'):
    TAGGED_RELEASE = True
    __version__ = PYNEQSYS_RELEASE_VERSION[1:]
else:
    TAGGED_RELEASE = False
    # read __version__ attribute from _release.py:
    exec(open(release_py_path).read())

classifiers = [
    "Development Status :: 3 - Alpha",
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
]

tests = [
    'pyneqsys.tests',
]

with open(os.path.join(pkg_name, '__init__.py')) as f:
    long_description = f.read().split('"""')[1]
descr = 'Solving of symbolic systems of non-linear equations numerically.'
setup_kwargs = dict(
    name=pkg_name,
    version=__version__,
    description=descr,
    long_description=long_description,
    classifiers=classifiers,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    url='https://github.com/bjodah/' + pkg_name,
    license='BSD',
    packages=[pkg_name] + tests
)

if __name__ == '__main__':
    try:
        if TAGGED_RELEASE:
            # Same commit should generate different sdist
            # depending on tagged version (set PYNEQSYS_RELEASE_VERSION)
            # this will ensure source distributions contain the correct version
            shutil.move(release_py_path, release_py_path+'__temp__')
            open(release_py_path, 'wt').write(
                "__version__ = '{}'\n".format(__version__))
        setup(**setup_kwargs)
    finally:
        if TAGGED_RELEASE:
            shutil.move(release_py_path+'__temp__', release_py_path)
