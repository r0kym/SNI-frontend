from django.shortcuts import render

from SNI.check import check_tokens
from SNI.error import render_error
from SNI.esi import post_universe_names
from SNI.lib import global_headers
from utils import SNI_URL

import requests


GLOBAL_URL = SNI_URL + "alliance"


@check_tokens(3)
def home(request):
    """
    Alliance home view
    """

    request_ally = requests.get(GLOBAL_URL, headers=global_headers(request))

    if request_ally.status_code != 200:
        return render_error(request_ally)

    return render(request, "alliance/home.html", {
        "alliances": request_ally.json(),
    })

@check_tokens(3)
def sheet(request, ally_id):
    """
    Alliance sheet
    """
    request_alliance = requests.get(GLOBAL_URL+f"/{ally_id}", headers=global_headers(request))
    if request_alliance.status_code != 200:
        return render_error(request_alliance)

    return render(request, "alliance/sheet.html",{
        "alliance_id": ally_id,
        "alliance": request_alliance.json(),
        "alliance_name": request_alliance.json()["alliance_name"],
    })

@check_tokens(3)
def tracking(request, ally_id):
    """
    Alliance tracking
    """

    url = GLOBAL_URL+f"/{ally_id}/tracking"
    request_track = requests.get(url, headers=global_headers(request))
    if request_track.status_code != 200:
        return render_error(request_track)

    request_alliance = requests.get(GLOBAL_URL+f"/{ally_id}", headers=global_headers(request))
    if request_alliance.status_code != 200:
        return render_error(request_alliance)

    return render(request, "alliance/tracking.html", {
        "tracking": request_track.json(),
        "alliance_id": ally_id,
        "alliance_name": request_alliance.json()["alliance_name"],
    })
