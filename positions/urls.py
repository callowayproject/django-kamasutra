from django.conf.urls.defaults import *

urlpatterns = patterns('position.views',
    (r'^add/(?P<position_name>[\w_-]+)/(?P<type>[\d]+)/(?P<id>[\d]+)/$', 'add'),
    (r'^remove/(?P<position_name>[\w_-]+)/(?P<type>[\d]+)/(?P<id>[\d]+)/$', 'remove'),
    (r'^(?P<position_id>.*)/order_content/$', 'order_content'),
)