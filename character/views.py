from django.shortcuts import render
from django.http import HttpResponse
from django.views.defaults import bad_request

from character.models import IdToName

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN
import SNI.esi as esi
from SNI.check import check_tokens
from SNI.lib import global_headers, get_clearance_level

import datetime
import requests
from bs4 import BeautifulSoup

from SNI.error import render_error

CORPORATION_HISTORY_LIMIT = 15  # for not overloading the page when people went in way too much corporations

GLOBAL_URL = SNI_URL + "user"
HISTORY_URL = SNI_URL + "esi/history/characters/"


@check_tokens()
def home(request):
    """
    Will display all the characters registered on the SNI
    """

    request_characters = requests.get(GLOBAL_URL, headers=global_headers(request))

    if request_characters.status_code != 200:
        return render_error(request_characters)

    character_list = request_characters.json()

    # Remove root from the list as it is not a truly valid character
    root = next((item for item in character_list if item["character_name"] == "root"), None)
    if root != None:
        character_list.remove(root)

    return render(request, 'character/home.html', {"character_list": character_list})

@check_tokens()
def sheet(request, character_id):
    """
    Will display the main page for accessing charachter informations
    """

    # Get data from ESI
    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    character = request_name.json()

    corp_history = esi.get_corporation_history(character_id)
    if corp_history.status_code != 200:
        return render_error(corp_history)
    if len(corp_history.json()) > CORPORATION_HISTORY_LIMIT:
        corp_history = corp_history.json()[0:CORPORATION_HISTORY_LIMIT-1]
        shortend_corp_hist = True
    else:
        shortend_corp_hist = False
    corp_history = corp_history.json()

    for corp in corp_history:
        corp_id = corp["corporation_id"]
        corp_name = IdToName.get_name(corp_id, "corporations")
        corp["corporation_name"] = corp_name
        start_date = datetime.datetime.strptime(corp["start_date"], "%Y-%m-%dT%H:%M:%S%z")
        corp["start_date"] = f"{start_date.day}/{start_date.month}/{start_date.year} , {start_date.hour}:{start_date.minute}"

    #Getting Clone location
    url = f"{SNI_URL}esi/latest/characters/{character_id}/clones/"
    data="{\"on_behalf_of\": "+ str(character_id) + "}"
    request_clone = requests.get(url, headers=global_headers(request), data=data)
    if request_clone.status_code != 200:
        return render_error(request_clone)

    clone_data = request_clone.json()["data"]

    clone_list = list()
    if "jump_clones" in clone_data:
        for clones in clone_data["jump_clones"]:
            if clones["location_type"] == "structure" :
                clone_list.append(IdToName.get_name(clones["location_id"], "universe/structures", request))
            elif clones["location_type"] == "station" :
                clone_list.append(IdToName.get_name(clones["location_id"], "universe/stations"))
            else:
                clone_list.append("this was unexpected, contact the site admin...")

    # Locatiom history
    url = HISTORY_URL + f"{character_id}/location/now"
    request_location = requests.post(url, headers=global_headers(request))

    return render(request, 'character/sheet.html', {
        "character_id": character_id,
        "character_name": character["name"],
        "character": character,
        "corp_history": corp_history,
        "shortend_corp_hist": shortend_corp_hist,
        "clone_list": clone_list,
        "clearance_level": get_clearance_level(request),
        "location": request_location,
    })

@check_tokens()
def sni(request, character_id):
    """
    Will display the SNI details for a character
    """

    #Get data from SNI backend
    url = f"{GLOBAL_URL}/{character_id}"
    request_sni = requests.get(url, headers=global_headers(request))
    if request_sni.status_code != 200:
        return render_error(request_sni)

    character = request_sni.json()

    # Get corporation details
    if character["corporation"]:
        corp_id = character["corporation"]
        corp_name = IdToName.get_name(corp_id, 'corporations')

        character["corporation"] = {
            "id": character["corporation"],
            "name": corp_name
        }

    else:
        character["corporation"] = {"name": ""}

    # Get alliance details
    if character["alliance"]:
        alliance_name = IdToName.get_name(character["alliance"], 'alliances')
        character["alliance"] = {
            "id": character["alliance"],
            "name": alliance_name,
        }
    else:
        character["alliance"] = {"name": ""}

    # Get coalition details
    resolved_coalition = list()
    if character["coalitions"]:
        for coalition in character["coalitions"]:
            url_coalition = f"{SNI_URL}coalition/{coalition}"
            request_coalition = requests.get(url_coalition, headers=global_headers(request))
            resolved_coalition.append({
                "id": coalition,
                "name": request_coalition.json()["coalition_name"]
            })

            #character["coalitions"][coalition] = request_coalition.json()["coalition_name"]
    character["coalitions"] = resolved_coalition

    return render(request, 'character/sni.html', {
        "character_id": character_id,
        "character_name": character["character_name"],
        "character": character,
    })

@check_tokens()
def assets(request, character_id):
    """
    Displays character assets
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    return render(request, 'character/assets.html', {
        "character": request_name.json(),
        "character_id": character_id,
    })

@check_tokens()
def contracts(request, character_id):
    """
    Displays character contracts
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    url = SNI_URL + f"esi/latest/characters/{character_id}/contracts/"
    json = {"on_behalf_of": request.session["user_id"], "all_pages": True}
    request_contracts = requests.get(url, headers=global_headers(request), json=json)
    if request_contracts.status_code != 200:
        return render_error(request_contracts)

    return render(request, 'character/contracts.html', {
        "character": request_name.json(),
        "character_id": character_id,
        "contracts": request_contracts.json()["data"],
    })

@check_tokens()
def contracts_details(request, character_id, contract_id):
    """
    Displays informations on a contract
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    url = SNI_URL + f"esi/latest/characters/{character_id}/contracts/"
    json = {"on_behalf_of": request.session["user_id"], "all_pages": True}
    request_contracts = requests.get(url, headers=global_headers(request), json=json)
    if request_contracts.status_code != 200:
        return render_error(request_contracts)

    for contract in request_contracts.json()["data"]:
        if contract["contract_id"] == contract_id:
            if contract["type"] != "courier":
                request_contract_items = requests.get(url+f"{contract_id}/items/", headers=global_headers(request), json=json)
                if request_contract_items.status_code != 200:
                    return render_error(request_contract_items)
                contract["contract_items"] = request_contract_items.json()["data"]
            return render(request, 'character/contracts-details.html', {
                "character": request_name.json(),
                "character_id": character_id,
                "contract": contract,
            })
    return render(request, "404.html")

@check_tokens()
def locations(request, character_id):
    """
    Displays characters location history
    """

    url = HISTORY_URL + f"{character_id}/location"
    headers = global_headers(request)
    request_locations = requests.get(url, headers=headers)
    if request_locations.status_code != 200:
        return render_error(request_locations)

    locations = [(
        request_locations.json()[i],
        datetime.datetime.strptime(request_locations.json()[i]["timestamp"][:-6], "%Y-%m-%dT%H:%M:%S.").__str__()
    ) for i in range(len(request_locations.json()))]

    return render(request, "character/locations.html",{
        "character_id": character_id,
        "locations": locations,
    })

@check_tokens()
def mails(request, character_id):
    """
    Displays character mails
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    request_mails = requests.get(SNI_URL+f"esi/history/characters/{character_id}/mail", headers=global_headers(request))
    if request_mails.status_code != 200:
        return render_error(request_mails)

    return render(request, 'character/mails.html', {
        "character": request_name.json(),
        "character_id": character_id,
        "mails": request_mails.json(),
    })

@check_tokens()
def mails_details(request, character_id, mail_id):
    """
    Displays informations on a mail
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    json = {"on_behalf_of": request.session["user_id"]}
    request_mail_info = requests.get(SNI_URL+f"esi/latest/characters/{character_id}/mail/{mail_id}/", headers=global_headers(request), json=json)
    if request_mail_info.status_code != 200:
        return render_error(request_mail_info)
    mail = BeautifulSoup(request_mail_info.json()["data"]["body"].replace("<br>", "\n"), "html.parser")

    return render(request, 'character/mails-details.html', {
        "character": request_name.json(),
        "character_id": character_id,
        "mail": mail.get_text(),
    })

@check_tokens()
def skills(request, character_id):
    """
    Displays character skils
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    return render(request, 'character/skills.html', {
        "character": request_name.json(),
        "character_id": character_id,
    })

@check_tokens()
def wallet_journal(request, character_id):
    """
    Displays character journal
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    journal_url = SNI_URL + f"esi/latest/characters/{character_id}/wallet/journal/"
    data = {"all_pages": True, "on_behalf_of": request.session.get("user_id")}
    request_wallet_journal = requests.get(journal_url, headers=global_headers(request), json=data)
    if request_wallet_journal.status_code != 200:
        return render_error(request_wallet_journal)

    return render(request, 'character/journal.html', {
        "character": request_name.json(),
        "character_id": character_id,
        "journal": request_wallet_journal.json()["data"],
    })

@check_tokens()
def wallet_transactions(request, character_id):
    """
    Displays a character transactions list
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        return render_error(request_name)

    transactions_url = SNI_URL + f"esi/latest/characters/{character_id}/wallet/transactions/"
    json = {"all_pages": True, "on_behalf_of": request.session.get("user_id")}
    request_wallet_transactions = requests.get(transactions_url, headers=global_headers(request), json=json)
    if request_wallet_transactions.status_code != 200:
        return render_error(request_wallet_transactions)

    return render(request, 'character/transactions.html', {
        "character": request_name.json(),
        "character_id": character_id,
        "transactions": request_wallet_transactions.json()["data"],
    })
