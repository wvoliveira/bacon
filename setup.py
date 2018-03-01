import os
import shutil
from codecs import open
from os.path import abspath, dirname, join
from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from bacon import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


def copy_conf():
    try:
        os.mkdir('/etc/bacon/')
    except FileExistsError:
        pass
    shutil.copy('./bacon/data/bacon.ini', '/etc/bacon/')


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        copy_conf()
        develop.run(self)


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        copy_conf()
        install.run(self)


setup(
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    name='bacon',
    python_requires='>3.4.1',
    version=__version__,
    description='Backup your files',
    long_description=long_description,
    url='https://github.com/wvoliveira/bacon',
    author='Wellington Oliveira',
    author_email='oliveira@live.it',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Systems Administration',
        'License :: MIT',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='backup python linux bacon',
    packages=find_packages('.', exclude=['docs', 'tests*']),
    package_data={'bacon': ['data/*.ini']},
    install_requires=['colorama'],
    extras_require={'test': ['coverage', 'pytest', 'pytest-cov']},
    entry_points={'console_scripts': ['bacon=bacon.cli:main']},
)
