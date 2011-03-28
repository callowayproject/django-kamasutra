.. _render_content:

=================
Rendering Content
=================

Because a position can contain any type of content type, we need to render 
each piece of content according to its type.

There are two ways you can render the content, one is via the template tag 
:ref:`render_position_content`, the other way is to call the 
`render` method of the PositionContent :ref:`api_positioncontent_functions`.

Templates
=========

Out of the box, rendering a piece of content will default to template 
`positions/render/default.html`. You can create content type specific 
templates in this same directory to act as defaults to that content type,
for example::

	positions/render/
		+ blog__blog.html
		+ blog__entry.html
		+ default.html
		+ stories__story.html
		
.. note::

	We assume the :ref:`setting_combine_string` is set to its default 
	of __ (double under score), for these examples
		
These templates are now the default content type specific templates that will 
be used instead of default.html.

If certain positions should be render differently than others you can create 
folders with the positions name, such as::

	positions/render/
		+ my_position/
			+ default.html
			
Just like before you can specify content type specific templates within the 
position::

	positions/render/
		+ my_position/
			+ blog__blog.html
			+ blog__entry.html
			+ default.html
			
If the same position is used for multiple sections you can add a suffix when 
using the :ref:`render_position_content`

.. code-block:: django

	{% render_position_content pc with suffix=custom %}

This will then look for a template with the suffix custom, for example::

	positions/render/my_position/blog__blog__custom.html

If none of these meet your needs, you can specify a completely custom 
template:

.. code-block:: django

	{% render_position_content pc with template=/myapp/positions/my_customtemplate.html %}

Template selector
-----------------

Here is the template list that is built in order to select the right template 
for the content being rendered

::
	
	1. <custom_template_path>
	2. positions/render/<position_name>/<app><combine_string><model><combine_string><suffix>.html
	3. positions/render/<position_name>/<app><combine_string><model>.html
	4. positions/render/<app><combine_string><model>.html
	4. positions/render/<position_name>/default.html
	5. positions/render/default.html
	
**Example List**, before ``django.template.loader.select_template`` is called

::
	
	[u'positions/render/home__opinion/stories__story__first.html', 
	 u'positions/render/home__opinion/stories__story.html', 
	 u'positions/render/stories__story.html', 
	 u'positions/render/home__opinion/default.html', 
	 u'positions/render/default.html']
