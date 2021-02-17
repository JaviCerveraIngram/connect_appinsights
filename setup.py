from os import path
from setuptools import setup


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as fhandle:
    README = fhandle.read()


setup(
    name='connect_appinsights',
    version='20.3.0',
    description='Azure Application Insights logging integration with CloudBlue Connect SDK',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Ingram Micro',
    author_email='connect-service-account@ingrammicro.com',
    keywords='connect sdk cloudblue ingram micro ingrammicro cloud automation azure appinsights application insights logging',
    packages=['connect_appinsights'],
    url='https://github.com/JaviCerveraIngram/connect_appinsights',
    license='Apache Software License',
    install_requires=['connect-sdk-haxe-port', 'opencensus-ext-azure==1.0.4', 'opencensus-ext-requests==0.7.3', 'opencensus-ext-logging==0.1.0']
)
