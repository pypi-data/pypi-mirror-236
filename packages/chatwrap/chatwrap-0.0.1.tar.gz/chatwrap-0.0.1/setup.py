#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = [ ]

test_requirements = ['pytest>=3', ]

setup(
    author="Rex Wang",
    author_email='1073853456@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Wrapper of ChatGPT web server",
    entry_points={
        'console_scripts': [
            'chatwrap=chatwrap.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description="Wrapper of ChatGPT web server",
    include_package_data=True,
    keywords='chatwrap',
    name='chatwrap',
    packages=find_packages(include=['chatwrap', 'chatwrap.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/RexWzh/ChatGPT-Wrapper',
    version='0.0.1',
    zip_safe=False,
)
