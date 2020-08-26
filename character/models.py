from django.db import models

from SNI.esi import post_universe_names, BASE_URL
from SNI.lib import global_headers
from utils import SNI_URL

from datetime import date
import requests

# Create your models here.

class IdToName(models.Model):
    """
    Model that will store any eve id with the associated name
    """

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    timestamp = models.DateField(auto_now=True)

    @classmethod
    def get_name(cls, id, route=None, request=None):
        """
        Will look through the db if the id is known. If yes returns the name else go look on the ESI
        and saves the name.
        Every 2 days the name will be checked again in case it was changed.

        id: the id of the object
        route: string specifying the ESI path to look after the object
            ie: an id 20000029 and a route "universe/constellations" will make the request at
            `https://esi.evetech.net/latest/universe/constellations/20000029/`
            If none is givent the path `/universe/names/` will be used
        request: current http request. Needed when the route is `universe/structures` because an ESI access is needed
            for that endpoint
        """

        def find_name(id, route, request):
            """
            Will look on the ESI for  the name of an object.
            """

            if route == "universe/structures":
                url = SNI_URL + f"esi/latest/{route}/{id}/"  # done through SNI so that structures names can be found
                json = {"on_behalf_of": request.session.get("user_id")}
                r = requests.get(url, headers=global_headers(request), json=json)
            elif route:
                url = BASE_URL + f"{route}/{id}/"
                r = requests.get(url, headers={"accept":"application/json"})
            else:
                r = post_universe_names(id)

            if r.status_code == 200:
                if "name" in r.json():
                    return r.json()["name"]
                elif "data" in r.json() and "name" in r.json()["data"]:
                    return  r.json()["data"]["name"]
            return None

        try:
            obj = cls.objects.get(id=id)
        except cls.DoesNotExist:
            name = find_name(id, route, request)
            if name:
                obj = cls(name=name, id=id)
                obj.save()
            else:
                return f"Couldn't resolve {id} name"
        else:
            delta = obj.timestamp - date.today()
            if delta.days > 2:  # checks the name again
                name = find_name(id, route, request)
                if name:
                    obj = cls(name=name, id=id)
                    obj.save()
                else:
                    return f"Couldn't resolve {id} name"

        return obj.name

    def __str__(self):
        return self.name
