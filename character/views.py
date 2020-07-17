from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request

from character.models import CorporationName

import SNI.esi as esi
from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN


import datetime
import requests


CORPORATION_HISTORY_LIMIT = 15  # for not overloading the page when people went in way too much corporations


def home(request):
    """
    Will display all the characters registered on the SNI
    """

    url = SNI_URL + "user"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"

    }

    request_characters = requests.get(url, headers=headers)

    if request_characters.status_code == 200:
        character_list = request_characters.json()

        if "root" in character_list:
            character_list.remove("root")

        return render(request, 'character/home.html', {"character_list": character_list})
    else:
        return HttpResponse(f"""
        ERROR {request_characters.status_code} <br>
        {request_characters.json()}""")

def sheet(request, character_id):
    """
    Will display the main page for accessing charachter informations
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        raise Http404(request_name.json()["error"])

    corp_history = esi.get_corporation_history(character_id).json()
    if len(corp_history) > CORPORATION_HISTORY_LIMIT:
        corp_history = corp_history[0:CORPORATION_HISTORY_LIMIT-1]
        shortend_corp_hist = True
    else:
        shortend_corp_hist = False

    for corp in corp_history:
        corp_id = corp["corporation_id"]
        try:
            corp_name = CorporationName.objects.get(corporation_id=corp["corporation_id"]).corporation_name
        except CorporationName.DoesNotExist:
            corp_name_request = esi.post_universe_names(corp_id)
            corp_name = corp_name_request.json()[0]["name"]
            db_entry = CorporationName(corporation_id=corp_id, corporation_name=corp_name)
            db_entry.save()
        corp["corporation_name"] = corp_name
        start_date = datetime.datetime.strptime(corp["start_date"], "%Y-%m-%dT%H:%M:%S%z")
        corp["start_date"] = f"{start_date.day}/{start_date.month}/{start_date.year} , {start_date.hour}:{start_date.minute}"

    return render(request, 'character/sheet.html', {
        "character": request_name.json(),
        "character_id": character_id,
        "corp_history": corp_history,
        "shortend_corp_hist": shortend_corp_hist,
    })

def assets(request, character_id):
    """
    Displays character assets
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        raise Http404(request_name.json()["error"])

    return render(request, 'character/assets.html', {
        "character": request_name.json(),
        "character_id": character_id,
    })

def contracts(request, character_id):
    """
    Displays character contracts
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        raise Http404(request_name.json()["error"])

    return render(request, 'character/contracts.html', {
        "character": request_name.json(),
        "character_id": character_id,
    })

def mails(request, character_id):
    """
    Displays character mails
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        raise Http404(request_name.json()["error"])

    return render(request, 'character/mails.html', {
        "character": request_name.json(),
        "character_id": character_id,
    })

def skills(request, character_id):
    """
    Displays character skils
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        raise Http404(request_name.json()["error"])

    return render(request, 'character/skills.html', {
        "character": request_name.json(),
        "character_id": character_id,
    })

def wallet(request, character_id):
    """
    Displays character wallet
    """

    request_name = esi.get_character_information(character_id)
    if request_name.status_code != 200:
        raise Http404(request_name.json()["error"])

    return render(request, 'character/wallet.html', {
        "character": request_name.json(),
        "character_id": character_id,
    })
