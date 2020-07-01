from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request

from character.models import CorporationName

import SNI.esi as esi

import datetime


CORPORATION_HISTORY_LIMIT = 15  # for not overloading the page when people went in way too much corporations


def home(request, character_id):
    """
    Will display the main page for accessing charachter informations
    """

    request_name = esi.post_universe_names(character_id)
    if request_name.status_code == 200:
        if request_name.json()[0]["category"] == "character":
            character_name = request_name.json()[0]["name"]
        else:
            raise Http404("Not a character id")
    else:
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
        corp["start_date"] = f"{start_date.day}/{start_date.month}/{start_date.year} , {start_date.hour}/{start_date.minute}"

    return render(request, 'character/home.html', {
        "character_name": character_name,
        "character_id":character_id,
        "corp_history": corp_history,
        "shortend_corp_hist": shortend_corp_hist,
    })