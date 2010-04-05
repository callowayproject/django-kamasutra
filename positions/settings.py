from django.conf import settings

# Cache timeout for all position content
CACHE_TIMEOUT = getattr(settings, 'POSITION_CACHE_TIMEOUT', 60)
# Cache prefix for all postion keys
CACHE_PREFIX = getattr(settings, 'POSITION_CACHE_PREFIX', 'position')
# The amout of items to overlap the position.count variable
CONTENT_OVERLAP_COUNT = getattr(settings, 'POSITION_CONTENT_OVERLAP_COUNT', 2)
# String used to combine when retrieving a position via templatetags
CONBINE_STRING = getattr(settings, 'POSITION_PAGE_COMBINE_STRING', '__')

ADMIN_URL = getattr(settings, 'POSITION_ADMIN_URL', 'admin')

# List of templates per model
TEMPLATES = getattr(settings, "POSITION_TEMPLATES", {})