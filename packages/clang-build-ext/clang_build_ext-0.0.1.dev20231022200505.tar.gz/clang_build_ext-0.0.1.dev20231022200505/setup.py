#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'clang_build_ext',
        version = '0.0.1.dev20231022200505',
        description = 'Clang-based extension builder',
        long_description = '# Clang Build Extension\n\n[![Gitter](https://img.shields.io/gitter/room/karellen/Lobby?logo=gitter)](https://app.gitter.im/#/room/#karellen_Lobby:gitter.im)\n[![Build Status](https://img.shields.io/github/actions/workflow/status/karellen/clang-build-ext/build.yml?branch=master)](https://github.com/karellen/clang-build-ext/actions/workflows/build.yml)\n[![Coverage Status](https://img.shields.io/coveralls/github/karellen/clang-build-ext/master?logo=coveralls)](https://coveralls.io/r/karellen/clang-build-ext?branch=master)\n\n[![Clang Build Ext Version](https://img.shields.io/pypi/v/clang-build-ext?logo=pypi)](https://pypi.org/project/clang-build-ext/)\n[![Clang Build Ext Python Versions](https://img.shields.io/pypi/pyversions/clang-build-ext?logo=pypi)](https://pypi.org/project/clang-build-ext/)\n\n[![Clang Build Ext Downloads Per Day](https://img.shields.io/pypi/dd/clang-build-ext?logo=pypi)](https://pypistats.org/packages/clang-build-ext)\n[![Clang Build Ext Downloads Per Week](https://img.shields.io/pypi/dw/clang-build-ext?logo=pypi)](https://pypistats.org/packages/clang-build-ext)\n[![Clang Build Ext Downloads Per Month](https://img.shields.io/pypi/dm/clang-build-ext?logo=pypi)](https://pypistats.org/packages/clang-build-ext)\n\nThe `clang-build-ext` extension builds Python extensions using a Clang compiler stack.\nEither system LLVM/Clang or `karellen-llvm-clang` package can be used.\n\nBeyond compiler the additional functionality is currently undocumented.\n\n## How to Use\n\nAdd the followi \n```python \nfrom karellen.clang_build_ext import ClangBuildExt, ClangBuildClib\n\n...\n\nsetup(\n... \ncmdclass={"build_ext": ClangBuildExt,\n          "build_clib": ClangBuildClib},)\n)\n\n```',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3',
            'Operating System :: POSIX :: Linux',
            'Topic :: System :: Archiving :: Packaging',
            'Topic :: Software Development :: Build Tools',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta'
        ],
        keywords = 'setuptools extension cpythonclang c cpp cxx c++ compile',

        author = 'Karellen, Inc.',
        author_email = 'supervisor@karellen.co',
        maintainer = 'Arcadiy Ivanov',
        maintainer_email = 'arcadiy@karellen.co',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/karellen/clang-build-ext',
        project_urls = {
            'Bug Tracker': 'https://github.com/karellen/clang-build-ext/issues',
            'Documentation': 'https://github.com/karellen/clang-build-ext/',
            'Source Code': 'https://github.com/karellen/clang-build-ext/'
        },

        scripts = [],
        packages = ['karellen.clang_build_ext'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {
            'distutils.commands': ['build_ext = karellen.clang_build_ext:ClangBuildExt']
        },
        data_files = [],
        package_data = {
            'karellen/clang_build_ext': ['LICENSE']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.7',
        obsoletes = [],
    )
