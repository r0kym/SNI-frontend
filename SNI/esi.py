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

def post_universe_ids(*args):
    """
    Resolve a set of names to IDs in the following categories: agents, alliances, characters, constellations,
    corporations factions, inventory_types, regions, stations, and systems.
    Only exact matches will be returned.
    """

    url = BASE_URL + "universe/ids?datasource=tranquility"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    data = "["
    for name in args:
        data += f"\"{name}\","
    data = data[:-1] + "]"

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

def get_search(search, categories):
    """
    Search for entities that match the given string.

    params:
        search: the string you're looking for
        categories: Type of entities to search for.
            Available values : agent, alliance, character, constellation, corporation, faction, inventory_type,
            region, solar_system, station
            Must be entered as a string seperated by commas. ex: categories="alliance,corporation"
    """

    url = BASE_URL + "search/"

    headers = {
        "accept": "application/json"
    }

    params = {
        "search": search,
        "categories": categories
    }

    response = requests.get(url, headers=headers, params=params)

    return response
