# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()

with open('test-requirements.txt') as reqs_file:
    test_requirements = reqs_file.read().splitlines()



setup(
    name='lumpy_log',
    version='0.1.0',
    description='Making Git Commits human readable by showing the important lumps of code.',
    author='Martyn Eggleton @ The Sheffield UTC Academy Trust',
    author_email='meggleton@utcsheffield.org.uk',
    url='https://github.com/UTCSheffield/lumpy_log',
    license='MIT',
    entry_points={
        'console_scripts': [
            'lumpy_log=lumpy_log:main',
        ],
    },
    py_modules = ['lumpy_log'],
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={
        # If any package contains *.txt files, include them:
        "": ["*.yml", "*.hbs"],
    },
    python_requires='>=3.5',
    install_requires=requirements,
    tests_require=requirements + test_requirements,
    test_suite='nose2.collector.collector',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Documentation",
    ],
    keywords=["documentation", "git"],
)
