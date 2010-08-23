from django.conf.urls.defaults import *

urlpatterns = patterns('positions.views',
    url(regex=r'^add/(?P<position_name>[\w_-]+)/(?P<type>[\d]+)/(?P<id>[\d]+)/$',
        view="add",
        name="positions_add"),
        
    url(regex=r'^remove/(?P<position_name>[\w_-]+)/(?P<type>[\d]+)/(?P<id>[\d]+)/$',
        view="remove",
        name="positions_remove"),
        
    url(regex=r'^(?P<position_id>.*)/order_content/$',
        view="order_content",
        name="positions_ordercontent"),
        
    url(regex=r'^json/(?P<content_type_id>.*)/(?P<object_id>.*)/$',
        view="json_data",
        name="positions_jsondata"),
        
    url(regex=r'^$',
        view='index',
        name='positions_index')
)