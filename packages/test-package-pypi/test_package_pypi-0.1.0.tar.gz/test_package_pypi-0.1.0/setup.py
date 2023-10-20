
from setuptools import setup, find_packages


setup(
    name='test_package_pypi',
    version='0.1.0',
    description='A brief description of your package',
    author='Saro',
    author_email='lovito@qi4m.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.rst'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
