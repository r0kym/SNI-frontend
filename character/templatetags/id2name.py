from django import template
from character.models import IdToName


register = template.Library()


@register.simple_tag
def esi_name(id, route=None, request=None):
    """
    Will use the model IdToName to get the name of something
    """
    if route in ("universe/stations", "universe/structures"):
        choices = ("universe/stations", "universe/structures")
    elif route in ("characters", "corporations", "alliances"):
        choices = ("characters", "corporations", "alliances")
    else:
        choices = (route,)

    for choice in choices:
        name = IdToName.get_name(id, choice, request)
        if name != f"Couldn't resolve {id} name":
            break
    return name
