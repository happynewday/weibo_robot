#!/usr/bin/env python
#coding=utf8

try:
    from  setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
        name = 'weibo_robot',
        version = '1.0',
        install_requires = [], 
        description = 'python browser',
        url = 'https://github.com/zhouxianggen/weibo_robot', 
        author = 'zhouxianggen',
        author_email = 'zhouxianggen@gmail.com',
        classifiers = [ 'Programming Language :: Python :: 3.7',],
        packages = ['weibo_robot'],
        data_files = [ ], 
        )

