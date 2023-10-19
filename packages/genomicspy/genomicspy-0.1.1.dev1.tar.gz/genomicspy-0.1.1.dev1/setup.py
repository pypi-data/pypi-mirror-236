#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# with open('requirements.txt') as requirements_file:
#     requirements = [line.strip() for line in requirements_file]
requirements = []
test_requirements = [ ]

setup(
    author="Vivian Leung",
    author_email='leung.vivian.w@gmail.com',
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    description="Tools for manipulating vcfs doing genomics work",
    entry_points={
        'console_scripts': [
            'genomicspy=genomicspy.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT License",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['genomicspy', 'vcf', 'genomics'],
    name='genomicspy',
    packages=find_packages(include=['genomicspy', 'genomicspy.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/vivianleung/genomicspy',
    version='0.1.1dev1',
    zip_safe=False,
)
