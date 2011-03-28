from django.db.models import get_model
from django.template import Library, Node, TemplateSyntaxError, Variable, VariableDoesNotExist
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from positions.models import Position, PositionContent
from positions import settings as position_settings

register = Library()

def _parse_arguments(value):
    if not isinstance(value, unicode):
        return {}
        
    ret = {}
    for item in value.split(','):
        if len(item.split('=')) == 2:
            name, val = item.split('=')
            ret[name] = val
            
    return ret

def resolve_variable(value, context, none_on_fail=False):
    """
    A wrapper function to resolve template variables. 
    Will return None if [none_on_fail] is [True], otherwise
    it will return [value]
    """
    try:
        return Variable(value).resolve(context)
    except Exception:
        if none_on_fail: return None
        return value

class PositionContentNode(Node):
    def __init__(self, position, varname, **kwargs):
        self.position = position
        self.varname = varname
        self.limit = int(kwargs.get('limit', '0'))
        self.as_contenttype = True
        if str(kwargs.get('as_contenttype', 'True')).lower() == 'false':
            self.as_contenttype = False
    
    def render(self, context):
        pos = resolve_variable(self.position, context)
        context[self.varname] = Position.objects.get_content(
            position=pos, 
            count=self.limit, 
            as_contenttype=self.as_contenttype)
        return ""
    

class ApplicablePositionsNode(Node):
    def __init__(self, obj=None, content_type_id=None, object_id=None, varname=None, return_all=False):
        (self.obj, self.varname, self.return_all) = (obj, varname, return_all)
        (self.content_type_id, self.object_id) = (content_type_id, object_id)
    
    def render(self, context):
                
        obj = resolve_variable(self.obj, context, none_on_fail=True)
        content_type_id = resolve_variable(self.content_type_id, context)
        object_id = resolve_variable(self.object_id, context)
            
        if not obj:
            try:
                ctype = ContentType.objects.get(pk=str(content_type_id))
                obj = ctype.get_object_for_this_type(pk=str(object_id))
            except:
                pass

        context[self.varname] = Position.objects.get_applicable(obj, self.return_all)
        
        return "" 
        

class ContentPositionsNode(Node):
    def __init__(self, obj=None, content_type_id=None, object_id=None, varname=None):
        (self.obj, self.varname) = (obj, varname)
        (self.content_type_id, self.object_id) = (content_type_id, object_id)
    
    def render(self, context):
        
        obj = resolve_variable(self.obj, context, none_on_fail=True)
        content_type_id = resolve_variable(self.content_type_id, context)
        object_id = resolve_variable(self.object_id, context)
            
        if not obj:
            try:
                ctype = ContentType.objects.get(pk=str(content_type_id))
                obj = ctype.get_object_for_this_type(pk=str(object_id))
            except:
                pass
        
        context[self.varname] = Position.objects.positions_for_object(obj)
        
        return "" 
        
        
class PositionNode(Node):
    def __init__(self, prefix, name, varname, **kwargs):
        self.name = name
        self.prefix = prefix
        self.varname = varname
        self.slugify = False
        if str(kwargs.get('slugify', 'True')).lower() == 'true':
            self.slugify = True
        
    def render(self, context):
        
        name = resolve_variable(self.name, context)
        if self.slugify:
            name = slugify(name)
            
        prefix = resolve_variable(self.prefix, context)
        if self.slugify:
            prefix = slugify(prefix)
            
        s_name = name
        if prefix:
            s_name = '%s%s%s' % (prefix, position_settings.CONBINE_STRING, name)
        
        context[self.varname] = None
        try:
            position = Position.objects.get(name__iexact=s_name)
            context[self.varname] = position
        except Position.DoesNotExist:
            pass
                        
        return ""
        

class RenderPositionContentNode(Node):
    def __init__(self, pc, template=None, suffix=None):
        self.pc = pc
        self.template = template
        self.suffix = suffix
        
    def render(self, context):
        suffix, template = self.suffix, self.template
        
        pc = resolve_variable(self.pc, context)
        if not isinstance(pc, PositionContent):
            return None
            
        tpl = pc.render(template=template, suffix=suffix, 
            context_instance=context)
                        
        return tpl
        
        
class CanBePositionedNode(Node):
    def __init__(self, obj=None, content_type_id=None, object_id=None, varname=None):
        self.obj, self.content_type_id = obj, content_type_id
        self.object_id, self.varname = object_id, varname
        
    def render(self, context):
        
        obj = resolve_variable(self.obj, context, none_on_fail=True)
        content_type_id = resolve_variable(self.content_type_id, context)
        object_id = resolve_variable(self.object_id, context)
            
        if not obj:
            try:
                ctype = ContentType.objects.get(pk=str(content_type_id))
                obj = ctype.get_object_for_this_type(pk=str(object_id))
            except:
                pass
                
        if obj:
            context[self.varname] = Position.objects.can_be_positioned(obj)
        else:
            context[self.varname] = False
            
        return ""
        
        
def do_get_position_content(parser, token):
    """
    {% get_position_content position as content %}
    {% get_position_content position as content [limit=N] [as_contenttype=True|False] %}
    
    Where position is either a Position instance (e.g. position), or Position name (e.g. home__headlines).
    """
    argv = token.contents.split()
    argc = len(argv)
    
    if argc < 4:
        raise TemplateSyntaxError, "Tag %s takes at least 3 arguments." % argv[0]
    
    if argv[2] != 'as':
        raise TemplateSyntaxError, "Tag %s must have 'as' as the second argument." % argv[0]
        
    (position, varname) = (argv[1], argv[3])
    
    kwargs = {}
    for argument in argv[4:]:
        if len(argument.split('=')) == 2:
            kwargs[str(argument.split('=')[0])] = argument.split('=')[1]
    
    return PositionContentNode(position, varname, **kwargs)

def do_get_applicable_positions(parser, token):
    """
    {% get_applicable_positions object as positions [all] %}
    
    or for the admin..
    
    {% get_applicable_positions content_type_id object_id as positions [all] %}
    
    all is optional and will return all, if it is not speficied only positions
    that the current object is not contained in will be returned
    """
    argv = token.contents.split()
    argc = len(argv)

    if argc > 6:
        raise TemplateSyntaxError, "Tag %s takes three, four or five arguments." % argv[0]

    return_all = False
    if argv[2] == "as":
        if argc == 5 and argv[4] == 'all':
            return_all = True
        return ApplicablePositionsNode(obj=argv[1], varname=argv[3], 
            return_all=return_all)
    elif argv[3] == "as":
        if argc == 6 and argv[5] == 'all':
            return_all = True
        return ApplicablePositionsNode(content_type_id=argv[1], 
            object_id=argv[2], varname=argv[4], return_all=return_all)
    else:
        raise TemplateSyntaxError, 'Second or Third argument must be "as"'
    
def do_get_content_positions(parser, token):
    """
    {% get_content_positions object as positions %}
    
    or for the admin..
    
    {% get_content_positions content_type_id object_id as positions %}
    """
    argv = token.contents.split()
    argc = len(argv)
 
    if argc != 4 and argc != 5:
        raise TemplateSyntaxError, "Tag %s takes three or four arguments." % ar
 
    if argv[2] == "as":
        return ContentPositionsNode(obj=argv[1], varname=argv[3])
    elif argv[3] == "as":
        return ContentPositionsNode(content_type_id=argv[1], 
            object_id=argv[2], varname=argv[4])
    else:
        raise TemplateSyntaxError, 'Second or Third argument must be "as"'
    
def do_get_position(parser, token):
    """
    {% get_position name as varname %}
    {% get_position prefix name as varname [slugify=True|False] %}
    """    
    argv = token.contents.split()
    argc = len(argv)

    if argc < 4:
        raise TemplateSyntaxError, "Tag %s takes at least 3 argument." % argv[0]
        
    if argv[2] != 'as' and argv[3] != 'as':
        raise TemplateSyntaxError, "Tag %s must have 'as' as the second or third argument." % argv[0]
        
    name, prefix, varname, startpos = '', '', '', 0
    if argv[2] == 'as':
        name = argv[1]
        varname = argv[3]
        startpos = 4
    elif argv[3] == 'as':
        prefix = argv[1]
        name = argv[2]
        varname = argv[4]
        startpos = 5
    
    kwargs = {}
    for argument in argv[startpos:]:
        if len(argument.split('=')) == 2:
            kwargs[str(argument.split('=')[0])] = argument.split('=')[1]
    
    return PositionNode(prefix, name, varname, **kwargs)
    
def do_render_position_content(parser, token):
    """
    {% render_position_content [PositionContent] [with] [suffix=S] [template=T] %}
    {% render_position_content pc %}
    {% render_position_content pc with suffix=custom %}
    {% render_position_content pc with template=mycustomtemplates/positions/custom.html %}
    
    Only suffix OR template can be specified, but not both.
    """
    argv = token.contents.split()
    argc = len(argv)
    
    if argc < 2 or argc > 4:
        raise TemplateSyntaxError, "Tag %s takes either two or four arguments." % argv[0]
        
    if argc == 2:
        return RenderPositionContentNode(argv[1])
    else:
        if argv[2] != 'with':
            raise TemplateSyntaxError, 'Second argument must be "with" for tag %s.' % argv[0]
        extra = argv[3].split('=')
        if len(extra) != 2:
            raise TemplateSyntaxError, "Last argument must be formated correctly for tag %s." % argv[0]
        if not extra[0] in ['suffix', 'template']:
            raise TemplateSyntaxError, "Last argment must of either suffix or template for tag %s." % argv[0]
            
        kwargs = {str(extra[0]): extra[1],}
        return RenderPositionContentNode(argv[1], **kwargs)
    
def do_can_be_positioned(parser, token):
    """
    {% can_be_positioned [object] as [varname] %}
    {% can_be_positioned [content_type_id] [object_id] as [varname] %}
    {% can_be_positioned story as story_can_be_positioned %}
    {% can_be_positioned 23 1232 as object_can_be_positioned %}
    """
    argv = token.contents.split()
    argc = len(argv)
    
    if argc < 4 or argc > 5:
        raise TemplateSyntaxError, "Tag %s takes either 3 or 4 arguments," % argv[0]
        
    if argc == 4:
        if argv[2] != "as":
            raise TemplateSyntaxError, 'Second argument must be "as" for tag %s.' % argv[0]
        return CanBePositionedNode(obj=argv[1], varname=argv[3])
    elif argc == 5:
        if argv[3] != "as":
            raise TemplateSyntaxError, 'Third argument must be "as" for tag %s.' % argv[0]
        return CanBePositionedNode(content_type_id=argv[1], object_id=argv[2], varname=argv[4])
        
register.tag("get_position_content", do_get_position_content)
register.tag("get_content_positions", do_get_content_positions)
register.tag("get_applicable_positions", do_get_applicable_positions)
register.tag("get_position", do_get_position)
register.tag("render_position_content", do_render_position_content)
register.tag("can_be_positioned", do_can_be_positioned)
