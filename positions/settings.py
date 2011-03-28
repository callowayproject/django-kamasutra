from django.conf import settings

# The amout of items to overlap the position.count
CONTENT_OVERLAP_COUNT = getattr(settings, 'POSITION_CONTENT_OVERLAP_COUNT', 2)

# String used to combine when retrieving a position via templatetags
CONBINE_STRING = getattr(settings, 'POSITION_COMBINE_STRING', '__')

# List of templates per model
# EX: {"stories.story": "customtemplates/stories/position_render.html"}
# TEMPLATES = getattr(settings, "POSITION_TEMPLATES", {})