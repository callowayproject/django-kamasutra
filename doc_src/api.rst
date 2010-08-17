.. _api:

API
===

.. _api_position:

Position
--------

=================  ================  =============================================================
Attributes
--------------------------------------------------------------------------------------------------
Attribute          Type              Extra
=================  ================  =============================================================
name               SlugField
count              IntegerField      default=1
eligible_types     ManyToManyField   to django.contrib.contenttypes.models.ContentType
allow_all_types    BooleanField      default=False
description        TextField         blank=True
=================  ================  =============================================================

.. _api_positioncontent:

PositionContent
---------------

=================  ==================  =============================================================
Attributes
----------------------------------------------------------------------------------------------------
Attribute          Type                Extra
=================  ==================  =============================================================
position           ForeignKey          to positions.models.Position
content_type       ForeignKey          to django.contrib.contenttypes.models.ContentType
object_id          CharField
content_object     GenericForeignKey
order              IntegerField        default=1
add_date           DateTimeField       default=default=datetime.datetime.now
=================  ==================  =============================================================

Functions
~~~~~~~~~

=================  =================================================================================
Methods
----------------------------------------------------------------------------------------------------
Method             Description
=================  =================================================================================
render             renders the content object according to its content type
=================  =================================================================================   
   