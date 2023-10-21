# -*- coding: utf-8 -*-
#
# (C) Copyright IBM 2023.
#
"""Quadratic functions
"""

import os
import sys
import setuptools


MAJOR = 0
MINOR = 1
MICRO = 0

ISRELEASED = False
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

REQUIREMENTS = []
with open("requirements.txt") as f:
    for line in f:
        req = line.split('#')[0]
        if req:
            REQUIREMENTS.append(req)

PACKAGES = setuptools.find_namespace_packages()
PACKAGE_DATA = {
}

DOCLINES = __doc__.split('\n')
DESCRIPTION = DOCLINES[0]
LONG_DESCRIPTION = "\n".join(DOCLINES[2:])


def git_short_hash():
    try:
        git_str = "+" + os.popen('git log -1 --format="%h"').read().strip()
    except:  # pylint: disable=bare-except
        git_str = ""
    else:
        if git_str == '+': #fixes setuptools PEP issues with versioning
            git_str = ''
    return git_str

FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.dev'+str(MICRO)+git_short_hash()

def write_version_py(filename='quadratic_programs/version.py'):
    cnt = """\
# THIS FILE IS GENERATED FROM QUADRATIC_PROGRAMS SETUP.PY
# pylint: disable=invalid-name, missing-module-docstring
short_version = '%(version)s'
version = '%(fullversion)s'
release = %(isrelease)s
"""
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION, 'fullversion':
                       FULLVERSION, 'isrelease': str(ISRELEASED)})
    finally:
        a.close()

local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(local_path)
sys.path.insert(0, local_path)
sys.path.insert(0, os.path.join(local_path, 'quadratic_programs'))  # to retrive _version

# always rewrite _version
if os.path.exists('quadratic_programs/version.py'):
    os.remove('quadratic_programs/version.py')

write_version_py()


setuptools.setup(
    name='quadratic_programs',
    version=VERSION,
    packages=PACKAGES,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url="",
    author="IBM Quantum",
    author_email="paul.nation@ibm.com",
    license="Apache 2.0",
    classifiers=[
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=REQUIREMENTS,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    zip_safe=False
)
