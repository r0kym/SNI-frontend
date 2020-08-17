from django import template
from character.models import IdToName


register = template.Library()


@register.simple_tag
def esi_name(id, route=None, request=None):
    """
    Will use the model IdToName to get the name of something
    """
    try:
        name = IdToName.get_name(id, route, request)
        if "Couldn't find" in name and route == "universe/stations":
            name = IdToName.get_name(id, "universe/structures", request)
        elif "Couldn't find" in name and route == "universe/structures":
            name = IdToName.get_name(id, "universe/stations", request)
        return name
    except:
        return f"Error when loading the name of {id}"
