from django.conf import settings

# The amout of items to overlap the position.count
CONTENT_OVERLAP_COUNT = getattr(settings, 'POSITION_CONTENT_OVERLAP_COUNT', 2)

# String used to combine when retrieving a position via templatetags
CONBINE_STRING = getattr(settings, 'POSITION_COMBINE_STRING', '__')

# Setting that tells the view that if a position content is added or removed 
# update that ojects history
UPDATE_OBJECT_HISTORY = getattr(settings, 'POSITION_UPDATE_OBJECT_HISTORY', False)

# Setting that if True wil Update the posistion history if posistion content is added
# removed or re-ordered
UPDATE_POSITION_HISTORY = getattr(settings, 'POSITION_UPDATE_POSITION_HISTORY', False)
# List of templates per model
# EX: {"stories.story": "customtemplates/stories/position_render.html"}
# TEMPLATES = getattr(settings, "POSITION_TEMPLATES", {})