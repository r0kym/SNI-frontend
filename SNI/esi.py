"""
ESI related functions
"""


import requests


BASE_URL = "https://esi.evetech.net/latest/"


def post_universe_names(id):
    """
    Will send an id to the ESI and retrieve the name of the associated object
    """

    url = BASE_URL +  "universe/names/?datasource=tranquility"

    headers = {
         "accept": "application/json",
         "Content-Type": "application/json"
    }

    data = f"[{id}]"

    r = requests.post(url, headers=headers, data=data)
    try:
        return r.json()[0]["name"]
    except KeyError:
        print("Error when getting name:" + id)
        return "Couldn't get name"
