#!/usr/bin/python3

from setuptools import setup
# import os
# my_path = os.path.abspath(__file__)
# os.chdir(os.normpath(os.path.join(my_path, os.pardir)))

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='trans_jenkins',
    version='0.0.1',
    description='Integration python library for transexual jenkins',
    package_dir={'':'py_trans_jenkins'},
    packages=['trans_jenkins', 'trans_jenkins.src', 'trans_jenkins.examples'],
    url='',
    python_requires=">=3.8.3",
    license='',
    author='mikey strauss',
    author_email='mdstrauss91@gmail.com',
    install_requires=['pandas',
                    'pandas-datareader',
                    'matplotlib',
                    'plotly',
                    'pandas-profiling',
                    'sweetviz']
)
