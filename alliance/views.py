from django.shortcuts import render, reverse, redirect

from SNI.check import check_tokens
from SNI.error import render_error
from SNI.esi import post_universe_names, ESI_SCOPES
from SNI.lib import global_headers
from utils import SNI_URL

import requests
from urllib.parse import urlencode


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
        "changed_scopes": request.GET.get("changed_scopes"),
        "alliance_id": ally_id,
        "alliance": request_alliance.json(),
        "alliance_name": request_alliance.json()["alliance_name"],
        "scopes": ESI_SCOPES,
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

@check_tokens(4)
def change_scopes(request, ally_id):
    """
    Changing alliance mandatory scopes with a specific list
    """

    scopes = []
    for key in request.POST:
        if key in ESI_SCOPES:
            scopes.append(key)

    if len(scopes) > 0:
        data = "{\"mandatory_esi_scopes\": [\"" + "\",\"".join(scopes) + "\"]}"
    else:
        data = "{\"mandatory_esi_scopes\": []}"
    request_change = requests.put(GLOBAL_URL+f"/{ally_id}", headers=global_headers(request, {"Content-type":"application/json"}), data=data)
    if request_change.status_code != 200:
        return render_error(request_change)

    params = urlencode({"changed_scopes": "true"})
    return_url = reverse("alliance-sheet", args=[ally_id]) + "?" + params
    return redirect(return_url)

@check_tokens(4)
def change_scopes_all(request, ally_id):
    """
    Changing alliance mandatory scopes by applying them all
    """

    data = "{\"mandatory_esi_scopes\": [\"" + "\",\"".join(ESI_SCOPES) + "\"]}"
    request_change = requests.put(GLOBAL_URL+f"/{ally_id}", headers=global_headers(request, {"Content-type":"application/json"}), data=data)
    if request_change.status_code != 200:
        return render_error(request_change)

    params = urlencode({"changed_scopes": "true"})
    return_url = reverse("alliance-sheet", args=[ally_id]) + "?" + params
    return redirect(return_url)

@check_tokens(4)
def change_scopes_none(request, ally_id):
    """
    Changing alliance mandatory scopes by removing them all
    """

    data = "{\"mandatory_esi_scopes\": []}"
    request_change = requests.put(GLOBAL_URL+f"/{ally_id}", headers=global_headers(request, {"Content-type":"application/json"}), data=data)
    if request_change.status_code != 200:
        return render_error(request_change)

    params = urlencode({"changed_scopes": "true"})
    return_url = reverse("alliance-sheet", args=[ally_id]) + "?" + params
    return redirect(return_url)
