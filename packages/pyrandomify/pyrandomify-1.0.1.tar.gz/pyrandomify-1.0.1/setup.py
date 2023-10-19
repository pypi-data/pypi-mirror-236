from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyrandomify',
    version='1.0.1',
    description='A simple module for convenient and fast generation of a character set',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="random randomify python-random",
    url='https://github.com/frymex/randomify',
    author='Nikita Protect',
    author_email='t_frymex@proton.me',
    license='BSD 2-clause',
    packages=['randomify'],
    install_requires=[],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
