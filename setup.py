import os

from setuptools import setup

description = 'Windows Jump Lists helper library'

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='jumplists',
    version='0.1.0',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/qermit/jumplists',
    project_urls={'Source': 'https://github.com/qermit/jumplists'},
    author='Piotr Miedzik',
    author_email='qermit@sezamkowa.net',
    license='MIT',
    packages=['jumplists'],
    install_requires=['pywin32'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
)
