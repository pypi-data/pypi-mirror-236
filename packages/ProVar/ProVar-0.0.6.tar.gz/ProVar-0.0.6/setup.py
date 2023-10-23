from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Science/Research',
    'License :: Other/Proprietary License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python :: 3',
]

setup(
    name='ProVar',
    version='0.0.6',
    package_dir={'ProVar': '.'},
    packages=['ProVar'],
    description='procedural variable system',
    long_description='This package provides tools for working with probabilistic variants in genomics data.',
    long_description_content_type='text/markdown',
    url='',
    author='Alexander Eriksen',
    author_email='Alex.eriksen@live.no',
    license='Privat Lisence',
    classifiers=classifiers,
    keywords='procedural variable',
    install_requires=['']
)