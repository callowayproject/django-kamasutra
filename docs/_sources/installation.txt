
Installation
============

Using PIP::

	pip install django-kamasutra
	
or download the app `here <http://pypi.python.org/pypi/django-kamasutra/>`_ ::

	python setup.py install


Add **positions** to your settings **INSTALLED_APPS**::

    INSTALLED_APPS = (
        ...
        'positions',
        ...
    )
    
Run syncdb::

    >>> ./manage.py syncdb
