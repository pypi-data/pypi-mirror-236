from setuptools import setup, find_packages

setup(
    name='encodify',
    version='1.0.0',
    packages=find_packages(),
    author='Ishan Oshada',
    author_email="ic31908@gmail.com",
    description='A module for encoding and encrypting data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ishanoshada/encodify',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        # Add any required dependencies here
        'binascii',
        'gzip',
        'zlib',
        'base64',
        'marshal',
        'functools',
    ],
)
