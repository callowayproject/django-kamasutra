.. _position-templatetags:

Template Tags
=============

============
get_position
============

    Gets a position object given in string.
    
    **Syntax**:
    
    .. code-block:: django
    
        {% get_position [prefix] name as varname [slugify=True|False] %}
    
    **Example**:
    
    .. code-block:: django
        
        {% get_position name as varname %}
        
        {% get_position prefix name as varname %}
        
        {% get_position prefix name as varname slugify=True %}
        
    The second example will conbine the prefix with ``settings.PAGE_CONBINE_STRING`` and the name given.
    
    The name can also be variables
    
    .. code-block:: django
    
        {% get_position category.name someobject.name as my_position %}
        
    This templatetag can optionally have slugify as the last argument. This specifies weather or not to slugify the prefix and/or name. Default is ``False``


====================
get_position_content
====================

    Gets the content in order for the ``models.Position`` object provided.
    
    **Syntax**:
    
    .. code-block:: django
        
        {% get_position_content position as varname %}
        
        {% get_position_content position as varname [limit=N] [as_contenttype=True|False] %}
        
    Optionally specify ``limit`` to only return that number of objects. Default is ``position.count``
    
    Optionally specify ``as_contenttype`` ``True`` to return the content type instance or ``False`` to return the ``models.PositionContent`` instances. Default is ``True``.
        
    **Example**:
    
    .. code-block:: django
    
        {% load positiontags %}
        {% get_position_content my_position as content_list %}
        
        {{ my_position.name }} has the following objects in it:<br/>
        {% for content in content_list %}
            {{ content }}<br/>
        {% endfor %}
    
    
========================
get_applicable_positions
========================

    Gets a ``models.Position`` list for the object provided, for which the object can be assigned to.

    
    **Syntax**:
    
    .. code-block:: django
    
        {% get_applicable_positions object as varname [all] %}
        {% get_applicable_positions content_type_id object_id as positions [all] %}
        
    By default, all positions the object can be added to will be returned 
    excluding the positions the object is current in. If `all` is specified 
    then all positions, including the ones the object is currently in, will be
    returned.
        
    **Example**:
    
    .. code-block:: django
        
        {% get_applicable_positions my_object as position_list %}
        
        This object can be assigned to these positions:
        {% for position in position_list %}
            {{ position.name }}<br/>
        {% endfor %}
        
    If we don't have the object available, such as in the admin, we can specify the content type id and object id.
    
    .. code-block:: django
    
        {% get_applicable_positions content_type_id object_id as myobj_applicable_postions %}
        {% get_applicable_positions 21 3 as myobj_applicable_postions %}
        
        
=====================
get_content_positions
=====================

    Gets a :ref:`api_position` list that the spcified object is currently in.
    
    **Syntax**:
    
    .. code-block:: django
    
        {% get_content_positions object as positions %}
        {% get_content_positions content_type_id object_id as positions %}
    
        
=================
can_be_positioned
=================

    Returns True|False if the supplied object can be positioned by any current position.
    
    **Syntax**:
    
    .. code-block:: django
        
        {% can_be_positioned [object] as [varname] %}
        {% can_be_positioned [content_type_id] [object_id] as [varname] %}
        
    **Example**:
    
    .. code-block:: django
    
        {% can_be_positioned myobj as myobj_canbe_positioned %}
        
        {% if myobj_canbe_positioned %}
            {{ myobj }} can be positioned
        {% endif %}
        
    If we don't have the object available, such as in the admin, we can specify the content type id and object id.
    
    .. code-block:: django
    
        {% can_be_positioned content_type_id object_id as myobj_canbe_positioned %}
        {% can_be_positioned 21 3 as myobj_canbe_positioned %}