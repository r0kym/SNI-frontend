from django import template
from character.models import IdToName


register = template.Library()


@register.simple_tag
def esi_name(id, route=None, request=None):
    """
    Will use the model IdToName to get the name of something
    """
    try:
        return IdToName.get_name(id, route, request)
    except:
        return f"Error when loading the name of {id}"
