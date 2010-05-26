from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views.decorators.cache import cache_page, never_cache
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.core import urlresolvers
from django.core.cache import cache

import simplejson

from positions.models import Position, PositionContent
from positions.forms import PositionContentOrderForm
from positions import settings as position_settings

def get_admin_url(obj, fallback="/admin/positions/"):
    """
    Returns the admin URL for the specified object, so that add and remove
    requests may redirect back to the object for which the operation was
    performed.
    """
    if hasattr(obj, "_meta"):
        return "/%s/%s/%s/%s" % (position_settings.ADMIN_URL, obj._meta.app_label,
            obj._meta.module_name, obj.id)
    return fallback
 

def widget_data(request, content_type_id, object_id):
    c = ContentType.objects.get(id=content_type_id)
    obj = c.get_object_for_this_type(id=object_id)
    
    positions = Position.objects.get_applicable(obj)
    
    data = [{"id":pos.pk,"name":pos.name,"value":pos.name} for pos in positions if request.GET.get('term', "") in pos.name]
    
    return HttpResponse(simplejson.dumps(data),
                                    mimetype='application/json')
    
 
def add(request, position_name, type, id):
    try:
        position = Position.objects.get(name__iexact=position_name)
    except Position.DoesNotExist:
        raise Http404
        
    c = ContentType.objects.get(id=type)
    obj = c.get_object_for_this_type(id=id)
    if position not in Position.objects.get_applicable(obj):
        return HttpResponseForbidden("The object cannot be added to this position.")
    
    Position.objects.add_object(position, obj)
    
    return HttpResponseRedirect(get_admin_url(obj))
add = staff_member_required(add)


def remove(request, position_name, type, id):
    """
    Resolves the object by the specified content type and id, and removes it
    from the specified Position if it has already been added.
    """
    next = request.GET.get('next', '')
    try:
        position = Position.objects.get(name__iexact=position_name)
    except Position.DoesNotExist:
        raise Http404
        
    c = ContentType.objects.get(id=type)
    obj = c.get_object_for_this_type(id=id)
    
    Position.objects.remove_object(position=position, obj=obj)
    
    if not next:
        next = get_admin_url(obj)
        
    return HttpResponseRedirect(next)
remove = staff_member_required(remove)

def order_content(request, position_id, template_name='admin/positions/order.html'):
    
    try:
        position = Position.objects.get(pk=position_id)
    except Position.DoesNotExist:
        raise Http404
        
    forms = []
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/%s/positions/position/' % position_settings.ADMIN_URL)
        for content in position.positioncontent_set.all():
            form = PositionContentOrderForm(request.POST, instance=content, prefix=str(content.pk))
            forms.append(form)
            if form.is_valid():
                if form.cleaned_data['order'] >= 0:
                    form.save()
                else:
                    form.instance.delete()
            
        return HttpResponseRedirect('.')       
    else:
        for content in position.positioncontent_set.all():
            form = PositionContentOrderForm(instance=content, prefix=str(content.pk))
            form.fields['order'].label = mark_safe('<span class="position_order">%s</span> %s ' % (content.order+1, content))
            form.fields['order'].content = content
            form.fields['order'].content_edit = ""
            if content.content_object and hasattr(content.content_object, "_meta"):
                admin_url_name = "admin:%s_%s_change" % (content.content_object._meta.app_label, content.content_object._meta.module_name)
                form.fields['order'].content_edit = urlresolvers.reverse(admin_url_name, args=(content.content_object.pk,))
            forms.append(form)
    
    return render_to_response(template_name, 
                                {'position': position,
                                 'forms': forms,}, 
                                 context_instance=RequestContext(request))      
order_content = staff_member_required(order_content)
order_content = never_cache(order_content)

def purge_cache(request, position_id, template_name='admin/positions/purge_cache.html'):
    
    position = get_object_or_404(Position, pk=position_id)
        
    PositionContent.objects.rebuild_cache(position)
    
    return render_to_response(template_name,
                              {'position': position},
                              context_instance=RequestContext(request))
    
    
    