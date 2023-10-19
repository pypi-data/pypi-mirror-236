#FileName: setup.py
#FileDate: 2023-10-18
#FileDescription:
#    Setup file for library.
#----------------------------------------------------------------------------------
#FileHistory:
#| Ver.|  Date    |Author|                       Description                      |
#| 0.1 |2023-10-18| CMF  |                     Initial Version                    |
#----------------------------------------------------------------------------------
# Import Libraries
from setuptools import setup, find_packages

setup(
    name= 'fdcLogger',
    version='0.3',
    packages=find_packages(),
    intall_requires=[],
    description='Custom logging utility.',
    author='Charles Fitzmaurice',
    author_email='charles.fitzmaurice1993@gmail.com'
)