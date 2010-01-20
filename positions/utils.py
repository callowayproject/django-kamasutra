from positions import settings as position_settings

def get_cache_key(position, extra=''):
    from positions.models import Position
    
    if not isinstance(position, Position):
        return ''
        
    if not isinstance(extra, str):
        extra = ''
        
    return '%s.%s:%s' % (
        position_settings.CACHE_PREFIX, 
        str(position.pk), 
        extra or str(position.count))    