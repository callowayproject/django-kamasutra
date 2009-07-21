from django.conf import settings

# Cache timeout for all slot related content
CACHE_TIMEOUT = getattr(settings, 'SLOT_CACHE_TIMEOUT', 60)
# Cache prefix for all slot related keys
CACHE_PREFIX = getattr(settings, 'SLOT_CACHE_PREFIX', 'slots')
# The amout of items to overlap the slot.count variable
CONTENT_OVERLAP_COUNT = getattr(settings, 'SLOT_CONTENT_OVERLAP_COUNT', 2)

PAGE_SLOT_CONBINE_STRING = getattr(settings, 'SLOT_PAGE_SLOT_COMBINE_STRING', '__')
