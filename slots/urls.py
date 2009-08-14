from django.conf.urls.defaults import *

urlpatterns = patterns('slots.views',
    (r'^add/(?P<slotname>[\w_-]+)/(?P<type>[\d]+)/(?P<id>[\d]+)/$', 'add'),
    (r'^remove/(?P<slotname>[\w_-]+)/(?P<type>[\d]+)/(?P<id>[\d]+)/$', 'remove'),
    (r'^(?P<slot_id>.*)/order_content/$', 'order_content'),
)