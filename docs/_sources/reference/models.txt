
Models
======

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
allow_all_types    BooleanField      null=True, blank=True
description        TextField         blank=True
sites              ManyToManyField   to django.contrib.sites.models.Site
=================  ================  =============================================================


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


=================  =================================================================================
Methods
----------------------------------------------------------------------------------------------------
Method             Description
=================  =================================================================================
render             renders the content object according to its content type
=================  =================================================================================   
   