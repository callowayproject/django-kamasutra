import os
from setuptools import setup
import positions

version = positions.__version__

try:
    f = open('README.rst')
    long_desc = f.read()
    f.close()
except:
    long_desc = ""

try:
    reqs = open('requirements.txt').read()
except:
    reqs = ''
    
setup(name='django-kamasutra',
      version=version,
      description='A application to position objects anywhere on a page.',
      long_description=long_desc,
      author='Jose Soares',
      author_email='josefsoares@gmail.com',
      url='https://github.com/callowayproject/django-kamasutra',
      packages=['positions'],
      include_package_data = True,
      install_requires = reqs,
      classifiers=['Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          ],
      )
