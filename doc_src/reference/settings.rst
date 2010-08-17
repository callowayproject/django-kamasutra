.. _settings:

Settings
========

Below is a list of all the position settings

.. _setting_content_overlap_count:

==============================
POSITION_CONTENT_OVERLAP_COUNT
==============================

The number of objects to keep after the position has added more items then 
its position.count specified. Default is 2.

.. _setting_page_conbine_string:

=======================
POSITION_COMBINE_STRING
=======================

When retrieving a position with a prefix, this value is used to combine 
the prefix and the name. Default is '__' (2 underscores).

.. _setting_templates:

==================
POSITION_TEMPLATES
==================

Dictionary of templates to be used when rendering a item.

Example

.. code-block:: python

    POSITION_TEMPLATES = {
        'stories.story': 'customtemplates/positions/stories/story.html',
        'blogs.blog': 'blogs/positions/blog.html',
    
    }

 
