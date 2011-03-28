
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


Getting Started
===============

Creating your first position
----------------------------

The minimum required arguments to create a positions is a `name`, which is a `SlugField`.

::

    from positions.models import Position
    
    position = Position.objects.create(name="MyPosition")
    
    
Add something to your Position
------------------------------

The position manager has a `add_object` method that takes, at minimum, 2 arguments, `position` and `obj`

* **position** should be a `positions.Position` instance
* **obj** can be any model instance

::
    
    from myapp.models import MyApp
    
    obj = MyApp.objects.get_latest()

    Position.objects.add_object(position=position, obj=obj)
    
    
.. note::

    The `Position` model can define which types of objects that can be added. 
    Therefore when adding objects to a position, make sure the content types 
    is allowed by the `Position` instance.
    
Retrieve your position content
------------------------------

The position manager has a `get_content` method that takes at least 1 argument, `position`.

* **position** should be a `positions.Position` instance

::

    position = Position.objects.get(name="MyPosition")
    
    content = Position.objects.get_content(position=position)
    
    
Retrieve your position content via templatetag
----------------------------------------------

::

    {% get_position_content position as content %}
    
`get_position_content` expects [position] [as] [varname]

* **position** can be a positions.Position instance or a name of a position


::
    
    Position {{ position }} has the following content:<br/>
    <ul>
    {% for obj in content %}
        <li>{{ obj }}</li>
    {% endfor %}
    </ul>
    
.. note::

    By default the object instance will be returned, although returning the positions.PositionContent instance, which holds the generic relation between position and the object, is also possible
    
    ::
    
        {% get_position_content position as content as_content_type=False %}
        