"""
ESI related functions
"""


import requests


BASE_URL = "https://esi.evetech.net/latest/"

ESI_SCOPES = [
    "publicData",
    "esi-alliances.read_contacts.v1",
    "esi-assets.read_assets.v1",
    "esi-assets.read_corporation_assets.v1",
    "esi-bookmarks.read_character_bookmarks.v1",
    "esi-bookmarks.read_corporation_bookmarks.v1",
    "esi-calendar.read_calendar_events.v1",
    "esi-calendar.respond_calendar_events.v1",
    "esi-characters.read_agents_research.v1",
    "esi-characters.read_blueprints.v1",
    "esi-characters.read_chat_channels.v1",
    "esi-characters.read_contacts.v1",
    "esi-characters.read_corporation_roles.v1",
    "esi-characters.read_fatigue.v1",
    "esi-characters.read_fw_stats.v1",
    "esi-characters.read_loyalty.v1",
    "esi-characters.read_medals.v1",
    "esi-characters.read_notifications.v1",
    "esi-characters.read_opportunities.v1",
    "esi-characters.read_standings.v1",
    "esi-characters.read_titles.v1",
    "esi-characters.write_contacts.v1",
    "esi-characterstats.read.v1",
    "esi-clones.read_clones.v1",
    "esi-clones.read_implants.v1",
    "esi-contracts.read_character_contracts.v1",
    "esi-contracts.read_corporation_contracts.v1",
    "esi-corporations.read_blueprints.v1",
    "esi-corporations.read_contacts.v1",
    "esi-corporations.read_container_logs.v1",
    "esi-corporations.read_corporation_membership.v1",
    "esi-corporations.read_divisions.v1",
    "esi-corporations.read_facilities.v1",
    "esi-corporations.read_fw_stats.v1",
    "esi-corporations.read_medals.v1",
    "esi-corporations.read_standings.v1",
    "esi-corporations.read_starbases.v1",
    "esi-corporations.read_structures.v1",
    "esi-corporations.read_titles.v1",
    "esi-corporations.track_members.v1",
    "esi-fittings.read_fittings.v1",
    "esi-fittings.write_fittings.v1",
    "esi-fleets.read_fleet.v1",
    "esi-fleets.write_fleet.v1",
    "esi-industry.read_character_jobs.v1",
    "esi-industry.read_character_mining.v1",
    "esi-industry.read_corporation_jobs.v1",
    "esi-industry.read_corporation_mining.v1",
    "esi-killmails.read_corporation_killmails.v1",
    "esi-killmails.read_killmails.v1",
    "esi-location.read_location.v1",
    "esi-location.read_online.v1",
    "esi-location.read_ship_type.v1",
    "esi-mail.organize_mail.v1",
    "esi-mail.read_mail.v1",
    "esi-mail.send_mail.v1",
    "esi-markets.read_character_orders.v1",
    "esi-markets.read_corporation_orders.v1",
    "esi-markets.structure_markets.v1",
    "esi-planets.manage_planets.v1",
    "esi-planets.read_customs_offices.v1",
    "esi-search.search_structures.v1",
    "esi-skills.read_skillqueue.v1",
    "esi-skills.read_skills.v1",
    "esi-ui.open_window.v1",
    "esi-ui.write_waypoint.v1",
    "esi-universe.read_structures.v1",
    "esi-wallet.read_character_wallet.v1",
    "esi-wallet.read_corporation_wallet.v1",
    "esi-wallet.read_corporation_wallets.v1"
]

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

    data = "[\"" + "\",\"".join(args) + "\"]"

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

def get_corporations_corporation_id(corporation_id):
    """
    Retrives corporation public informations
    """

    url = BASE_URL + f"corporations/{corporation_id}/?datasource=tranquility"

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
