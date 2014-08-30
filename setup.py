#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import sys
import time
import subprocess
from setuptools import setup, find_packages, Command
from setuptools.command.test import test


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fp:
        return fp.read()


def runcmd(cmd):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE) as p:
        out, err = p.communicate()
    return out, err


class PyTest(test):
    def finalize_options(self):
        super(PyTest, self).finalize_options()
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


class GenerateVersionCommand(Command):
    description = 'generates a version file'
    user_options = [
            ('force=', 'f', 'force a specific version number')]

    def initialize_options(self):
        self.force = None

    def finalize_options(self):
        pass

    def run(self):
        v = self.force or generate_version()
        write_version(v)
        print("Generated version %s" % v)
        return 0


def generate_version():
    """ Generate a version file from the source control information.
        (this is loosely based on what Mercurial does)"""
    if not os.path.isdir(os.path.join(os.path.dirname(__file__), '.hg')):
        raise Exception("Can't generate version number: this is not a "
                        "Mercurial repository.")

    try:
        # Get the version we're currently on. Also see if we have local
        # changes.
        cmd = ['hg', 'id', '-i']
        hgid, err = runcmd(cmd)
        hgid = hgid.decode('utf8').strip()
        has_local_changes = hgid.endswith('+')
        hgid = hgid.rstrip('+')

        # Get the tags on the current version.
        cmd = ['hg', 'log', '-r', '.', '--template', '{tags}\n']
        tags, err = runcmd(cmd)
        versions = [t for t in tags.decode('utf8').split() if t[0].isdigit()]

        if versions:
            # Use the tag found at the current revision.
            version = versions[-1]
        else:
            # Use the latest tag, but add info about how many revisions
            # there have been since then.
            cmd = ['hg', 'parents', '--template',
                   '{latesttag}+{latesttagdistance}']
            version, err = runcmd(cmd)
            tag, dist = version.decode('utf8').split('+')
            if dist == '1':
                # We're on the commit that created the tag in the first place.
                # Let's just do as if we were on the tag.
                version = tag
            else:
                version = '%s-%s.%s' % (tag, dist, hgid)

        if has_local_changes:
            version += time.strftime('+%Y%m%d')

        return version
    except OSError:
        raise Exception("Can't generate version number: Mercurial isn't "
                        "installed, or in the PATH.")
    except Exception as ex:
        raise Exception("Can't generate version number: %s" % ex)


def write_version(version):
    if not version:
        raise Exception("No version to write!")

    f = open("piecrust/__version__.py", "w")
    f.write('# this file is autogenerated by setup.py\n')
    f.write('APP_VERSION = "%s"\n' % version)
    f.close()


# Always try to generate an up to date version.
# Otherwise, fall back on an (hopefully) existing version file.
try:
    version = generate_version()
    write_version(version)
except:
    version = None

if version is None:
    try:
        from piecrust.__version__ import APP_VERSION
        version = APP_VERSION
    except ImportError:
        raise Exception("Can't get version from either a version file or "
                        "from the repository.")


setup(name="PieCrust",
        version=version,
        description="A powerful static website generator and lightweight CMS.",
        long_description=read('README.rst') + '\n\n' + read('CHANGELOG.rst'),
        author="Ludovic Chabant",
        author_email="ludovic@chabant.com",
        license="Apache License 2.0",
        url="http://github.com/ludovicchabant/piecrust2",
        keywords=' '.join([
            'python',
            'website',
            'generator',
            'blog',
            'portfolio',
            'gallery',
            'cms'
            ]),
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'Jinja2==2.7.3',
            'Markdown==2.4.1',
            'MarkupSafe==0.23',
            'PyYAML==3.11',
            'Pygments==1.6',
            'Werkzeug==0.9.6',
            'colorama==0.3.1',
            'compressinja==0.0.2',
            'mock==1.0.1',
            'py==1.4.23',
            'python-dateutil==2.2',
            'repoze.lru==0.6',
            'strict-rfc3339==0.4'
            ],
        tests_require=[
            'pytest==2.6.1',
            'pytest-mock==0.2.0'
            ],
        cmdclass={
            'test': PyTest,
            'version' : GenerateVersionCommand
            },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'Natural Language :: English',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3'
            ],
        entry_points={'console_scripts': [
            'chef = piecrust.main:main',
            ]}
        )

