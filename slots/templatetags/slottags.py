from django.db.models import get_model
from django.template import Library, Node, TemplateSyntaxError, Variable, resolve_variable, VariableDoesNotExist
from slots.models import Slot, SlotContent
from django.utils.translation import ugettext as _

register = Library()

class SlotContentNode(Node):
    def __init__(self, slot, varname, count=None):
        (self.slot, self.varname, self.count) = (slot, varname, count)
        
    def render(self, context):
        try:
            slot = Variable(self.slot).resolve(context)
        except VariableDoesNotExist:
            try:
                slot = Slot.objects.get(name__iexact=self.slot)
            except:
                return ""

        objects = Slot.objects.get_content(slot=slot, count=self.count)
        context[self.varname] = objects
        return ""


class ApplicableSlotsNode(Node):
    def __init__(self, obj, varname):
        (self.obj, self.varname) = (obj, varname)
    
    def render(self, context):
        try:
            obj = Variable(self.obj).resolve(context)
        except VariableDoesNotExist:
            return ""
        
        context[self.varname] = Slot.objects.get_applicable(obj)
        return ""  
        
class ApplicableSlotClassNode(Node):
    def __init__(self, obj, slot):
        (self.obj, self.slot) = (obj, slot)
    
    def render(self, context):
        try:
            obj = Variable(self.obj).resolve(context)
            slot = Variable(self.slot).resolve(context)
        except VariableDoesNotExist:
            return ""
        
        if Slot.objects.contains_object(slot, obj):
            return "selected=\"true\""
        return ""   
        
        
def do_get_slot_content(parser, token):
    """
    {% get_slot_content slot as content %}
    {% get_slot_content slot as content count %}
    
    Where slot is either a Slot instance (e.g. slot), or Slot name (e.g. home__cube).
    """
    argv = token.contents.split()
    argc = len(argv)
    
    if argc != 4 and argc != 5:
        raise TemplateSyntaxError, "Tag %s takes three to four arguments." % argv[0]
    
    (slot, varname, count) = (argv[1], argv[3], None)
    
    if argc == 5:
        count = int(argv[5])
    
    return SlotContentNode(slot, varname, count)

def do_get_applicable_slots(parser, token):
    """
    {% get_applicable_slots object as slots %}
    """
    argv = token.contents.split()
    argc = len(argv)

    if argc != 4:
        raise template.TemplateSyntaxError, "Tag %s takes three arguments." % argv[0]

    return ApplicableSlotsNode(argv[1], argv[3])
    
def do_get_applicable_slot_class(parser, token):
    """
    {% get_applicable_slot_class object slot %}
    """
    argv = token.contents.split()
    argc = len(argv)

    if argc != 3:
        raise template.TemplateSyntaxError, "Tag %s takes two argument." % argv[0]

    return ApplicableSlotClassNode(argv[1], argv[2])
    
register.tag("get_slot_content", do_get_slot_content)
register.tag("get_applicable_slots", do_get_applicable_slots)
register.tag("get_applicable_slot_class", do_get_applicable_slot_class)
