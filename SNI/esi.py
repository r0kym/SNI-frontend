"""
ESI related functions
"""


import requests


BASE_URL = "https://esi.evetech.net/latest/"


def post_universe_names(*args):
    """
    Will send an id to the ESI and retrieve the name of the associated object
    """

    url = BASE_URL +  "universe/names/?datasource=tranquility"

    headers = {
         "accept": "application/json",
         "Content-Type": "application/json"
    }

    data = f"[{str(set(args))[1:-1]}]"  # removes duplicates

    response = requests.post(url, headers=headers, data=data)

    return response

def get_character_information(character_id):
    """
    Get Character public data
    """

    url = BASE_URL + f"characters/{character_id}?datasource=tranquility"
    
    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    return response


def get_corporation_history(character_id):
    """
    Retrieve the character's corporation histoy
    """

    url = BASE_URL + f"characters/{character_id}/corporationhistory?datasource=tranquility"

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    return response
