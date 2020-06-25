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

    response = requests.post(url, headers=headers, data=data)

    return response
