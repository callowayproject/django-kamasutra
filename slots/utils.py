from slots import settings

def get_cache_key(slot, extra=''):
    if not isinstance(extra, str):
        extra = ''
        
    if extra:
        return '%s.%s.%s:%s' % (settings.CACHE_PREFIX, str(slot.pk), str(slot.count), extra)
    else:
        return '%s.%s.%s' % (settings.CACHE_PREFIX, str(slot.pk), str(slot.count))          