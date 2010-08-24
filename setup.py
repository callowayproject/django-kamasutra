import os
from setuptools import setup, find_packages
import positions

try:
    reqs = open(os.path.join(os.path.dirname(__file__),'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''

setup(name='django-kamasutra',
      version=positions.get_version(),
      description='A generic featuring application.',
      author='Jose Soares',
      author_email='josefsoares@gmail.com',
      url='http://github.com/josesoa/django-kamasutra/',
      packages=find_packages(),
      include_package_data = True,
      install_requires = reqs,
      classifiers=['Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          'Development Status :: 4 - Beta',
          'Environment :: Other Environment',
          'Programming Language :: Python',
          ],
      )
