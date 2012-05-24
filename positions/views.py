from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views.decorators.cache import cache_page, never_cache
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.admin.models import ADDITION, DELETION, CHANGE, LogEntry
from django.utils.encoding import force_unicode
try:
    from django.utils import simplejson
except ImportError:
    simplejson = None

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
        return "/%s/%s/%s/%s" % (reverse("admin:index"), obj._meta.app_label,
            obj._meta.module_name, obj.id)
    return fallback

def index(request):
    """
    This is a dummy view so we can reverse the root url
    """
    raise Http404
    

def json_data(request, content_type_id, object_id):
    """
    This is used for the admin widget
    """
    if not simplejson:
        raise Http404
        
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    try:
        obj = ctype.get_object_for_this_type(id=object_id)
    except:
        raise Http404
    
    positions = Position.objects.get_applicable(obj)
    
    data = [{"id":pos.pk,"name":pos.name,"value":pos.name} for pos in positions if request.GET.get('term', "") in pos.name]
    
    return HttpResponse(simplejson.dumps(data),
                                    mimetype='application/json')
    
 
def add(request, position_name, type, id):
    
    position = get_object_or_404(Position, name__iexact=position_name)
    ctype = get_object_or_404(ContentType, pk=type)
    
    obj = ctype.get_object_for_this_type(id=id)
    if position not in Position.objects.get_applicable(obj):
        return HttpResponseForbidden("The object cannot be added to this position.")
    
    added_successfully = Position.objects.add_object(position, obj)
    if added_successfully:
        update_histories(request, obj, position, ADDITION)
    return HttpResponseRedirect(get_admin_url(obj))

add = staff_member_required(add)

def remove(request, position_name, type, id):
    """
    Resolves the object by the specified content type and id, and removes it
    from the specified Position if it has already been added.
    """
    next = request.GET.get('next', '')
    position = get_object_or_404(Position, name__iexact=position_name)
        
    ctype = get_object_or_404(ContentType, pk=type)
    obj = ctype.get_object_for_this_type(id=id)
    
    removed_successfully = Position.objects.remove_object(position=position, obj=obj)
    if removed_successfully:
        update_histories(request, obj, position, DELETION)
    
    if not next:
        next = get_admin_url(obj)
        
    return HttpResponseRedirect(next)
remove = staff_member_required(remove)

def order_content(request, position_id, template_name='admin/positions/order.html'):
    
    position = get_object_or_404(Position, pk=position_id)
        
    forms = []
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/%s/positions/position/' % reverse("admin:index"))
        
        re_order = False
        for content in position.positioncontent_set.all():
            original_order = content.order
            form = PositionContentOrderForm(request.POST, instance=content, prefix=str(content.pk))
            forms.append(form)
            if form.is_valid():
                if form.cleaned_data['order'] >= 0:
                    if form.cleaned_data['order'] != original_order:
                        re_order = True
                    form.save()
                else:
                    obj = form.instance
                    update_histories(request, obj.content_object, position, DELETION)
                    form.instance.delete()
        if re_order:
            update_position_history(request, None, position, CHANGE, "Position content was re-ordered.")
        return HttpResponseRedirect('.')       
    else:
        for content in position.positioncontent_set.all():
            form = PositionContentOrderForm(instance=content, prefix=str(content.pk))
            form.fields['order'].label = mark_safe('<span class="position_order">%s</span> %s ' % (content.order+1, content))
            form.fields['order'].content = content
            form.fields['order'].content_edit = ""
            if content.content_object and hasattr(content.content_object, "_meta"):
                admin_url_name = "admin:%s_%s_change" % (content.content_object._meta.app_label, content.content_object._meta.module_name)
                form.fields['order'].content_edit = reverse(admin_url_name, args=(content.content_object.pk,))
            forms.append(form)
    
    return render_to_response(template_name, 
                                {'position': position,
                                 'forms': forms,}, 
                                 context_instance=RequestContext(request))      
order_content = staff_member_required(order_content)
order_content = never_cache(order_content)
    
def update_histories(request, obj, position, action):
    """ Update both object history and posistion history """
    update_object_history(request, obj, position, action)
    update_position_history(request, obj, position, action)
    
def update_object_history(request, obj, position, action, message=None):
    """ Update object history if turned on """
    if not position_settings.UPDATE_OBJECT_HISTORY:
        return
    
    if not message:
        if action == ADDITION:
            action_message = 'added'
        elif action == DELETION:
            action_message = 'removed'
        else:
            action_message = 'changed'
        message = 'Position %s was %s. ' %(position, action_message)
        
    LogEntry.objects.log_action(
        user_id         = request.user.pk, 
        content_type_id = ContentType.objects.get_for_model(obj).pk,
        object_id       = obj.pk,
        object_repr     = force_unicode(obj), 
        action_flag     = action,
        change_message  = message
    )
    
def update_position_history(request, obj, position, action, message=None):
    """ Update position history if turned on """
    if not position_settings.UPDATE_POSITION_HISTORY:
        return
    
    if obj and not message:
        if action == ADDITION:
            action_message = 'added'
        elif action == DELETION:
            action_message = 'removed'
        else:
            action_message = 'changed'
        message = 'Position Content %s was %s.' %(obj, action_message)
        
    if not message:
        "Empty message."
        
    LogEntry.objects.log_action(
        user_id         = request.user.pk, 
        content_type_id = ContentType.objects.get_for_model(position).pk,
        object_id       = position.pk,
        object_repr     = force_unicode(position), 
        action_flag     = action,
        change_message  = message)
    