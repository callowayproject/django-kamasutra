from django.conf.urls.defaults import *

urlpatterns = patterns('positions.views',
    (r'^add/(?P<position_name>[\w_-]+)/(?P<type>[\d]+)/(?P<id>[\d]+)/$', 'add'),
    (r'^remove/(?P<position_name>[\w_-]+)/(?P<type>[\d]+)/(?P<id>[\d]+)/$', 'remove'),
    (r'^(?P<position_id>.*)/order_content/$', 'order_content'),
    (r'^widget/data/(?P<content_type_id>.*)/(?P<object_id>.*)/', 'widget_data')
)