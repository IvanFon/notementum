#!/usr/bin/env python3
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='notementum',
    version='0.1.0',
    description='A native, cross-platform, Markdown notebook app.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ivan Fonseca',
    author_email='ivanfon@riseup.net',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Editors',
        'Topic :: Utilities'
    ],
    keywords='markdown',
    packages=[
        'notementum',
        'notementum/views'
    ],
    install_requires=[
        'PyGObject',
        'mistletoe',
        'pygments',
    ],
    package_data={'notementum': ['res/*']},
    entry_points={
        'gui_scripts': [
            'notementum = notementum.__main__:main'
        ],
        'pygments.styles': [
            'notementum = notementum.highlight_style:NotementumStyle'
        ]
    }
)
