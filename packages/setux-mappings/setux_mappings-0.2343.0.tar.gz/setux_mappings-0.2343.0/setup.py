from os.path import join, dirname, abspath

from setuptools import setup, find_namespace_packages

curdir = abspath(dirname(__file__))
readme = open(join(curdir, 'README.md')).read()

setup(
    name             = 'setux_mappings',
    version          = '0.2343.0',
    description      = 'System deployment',
    long_description = readme,
    long_description_content_type='text/markdown',
    keywords         = ['utility', ],
    url              = 'https://notabug.org/dugres/setux_mappings',
    author           = 'Louis RIVIERE',
    author_email     = 'louis@riviere.xyz',
    license          = 'MIT',
    classifiers      = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    install_requires = [
        'setux_core>=0.2343.0',
    ],
    packages = find_namespace_packages(
        include=['setux.*']
    ),
)
