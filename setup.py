"""
Setup script for PyPi
"""

from distutils.core import setup
setup(
    name='scrapy-twitter',
    version='0.1',
    description='Twitter API wrapper for scrapy',
    url='http://github.com/yall/scrapy-twitter',
    author='Jonathan Geslin',
    author_email='jonathan.geslin@gmail.com',
    license='MIT',
    py_modules=['scrapy_twitter'],
    install_requires=[
        'python-twitter'
    ],
    zip_safe=False)