# Create your views here.


from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.views.decorators.cache import cache_page
from django.template.defaultfilters import slugify

from simpleapp.models import SimpleText, SimpleCategory
from positions.models import Position

def test(request, template_name='simpleapp/test.html'):
    
    cat1, created1 = SimpleCategory.objects.get_or_create(name='Test Category 1')
    cat2, created2 = SimpleCategory.objects.get_or_create(name='Test Category 2')
    
    text1, created3 = SimpleText.objects.get_or_create(firstname='Joe', lastname='Shmo', favorite_color='pink')
    text2, created4 = SimpleText.objects.get_or_create(firstname='James', lastname='Brown', favorite_color='brown')
    text3, created5 = SimpleText.objects.get_or_create(firstname='Roger', lastname='Green', favorite_color='green')
    text4, created6 = SimpleText.objects.get_or_create(firstname='Ben', lastname='Dean', favorite_color='yellow')
    text5, created7 = SimpleText.objects.get_or_create(firstname='Brad', lastname='Gurd', favorite_color='blue')
    text6, created8 = SimpleText.objects.get_or_create(firstname='Danny', lastname='Finch', favorite_color='orange')
    text7, created9 = SimpleText.objects.get_or_create(firstname='Steve', lastname='Turner', favorite_color='teal')
    text8, created10 = SimpleText.objects.get_or_create(firstname='Peter', lastname='Curry', favorite_color='black')

    position1, created11 = Position.objects.get_or_create(name='my_test_position', count=5, allow_all_types=True)
    
    position2, created12 = Position.objects.get_or_create(name=slugify(cat1.name), count=8, allow_all_types=True)
    
    position3, created13 = Position.objects.get_or_create(name='%s__%s' % (slugify(cat1.name), 'top_articles'), count=3, allow_all_types=True)


    if not len(position1.positioncontent_set.all()):
        Position.objects.add_object(position1, text1)
        Position.objects.add_object(position1, text2)
        Position.objects.add_object(position1, text3)
        Position.objects.add_object(position1, text4)
        Position.objects.add_object(position1, text5)
        
    if not len(position2.positioncontent_set.all()):
        Position.objects.add_object(position2, text3)
        Position.objects.add_object(position2, text2)
        Position.objects.add_object(position2, text8)
        Position.objects.add_object(position2, text4)
        Position.objects.add_object(position2, text5)
        Position.objects.add_object(position2, text1)
        Position.objects.add_object(position2, text6)
        Position.objects.add_object(position2, text7)

    if not len(position3.positioncontent_set.all()):
        Position.objects.add_object(position3, text2)
        Position.objects.add_object(position3, text4)
        Position.objects.add_object(position3, text3)
    
    return render_to_response(template_name,
                              {'cat1': cat1,
                               'cat2': cat2,
                               'text1': text1},
                              context_instance=RequestContext(request))
    