from django.shortcuts import render, reverse, redirect

from SNI.check import check_tokens
from SNI.error import render_error
from SNI.esi import post_universe_names, get_corporations_corporation_id, ESI_SCOPES
from SNI.lib import global_headers
from utils import SNI_URL

import requests
from urllib.parse import urlencode


GLOBAL_URL = SNI_URL + "corporation"


@check_tokens(1)
def home(request):
    """
    Corporation home
    """

    request_corp = requests.get(GLOBAL_URL, headers=global_headers(request))
    if request_corp.status_code != 200:
        return render_error(request_corp)

    return render(request, "corporation/home.html", {
        "corporations": request_corp.json(),
    })

@check_tokens(1)
def sheet(request, corp_id):
    """
    Information sheet on a corporation
    """

    request_corp = requests.get(GLOBAL_URL+f"/{corp_id}", headers=global_headers(request))
    if request_corp.status_code != 200:
        return render_error(request_corp)

    esi_request_corp = get_corporations_corporation_id(corp_id)
    if esi_request_corp.status_code != 200:
        return render_error(esi_request_corp)

    return render(request, "corporation/sheet.html", {
        "corporation": request_corp.json(),
        "esi": esi_request_corp.json(),
        "corporation_id": corp_id,
        "corporation_name": esi_request_corp.json()["name"],
        "scopes": ESI_SCOPES,
        "changed_scopes": request.GET.get("changed_scopes"),
    })

@check_tokens(1)
def tracking(request, corp_id):
    """
    Tracking of the corp membres tokens
    """
    url = GLOBAL_URL + f"/{corp_id}/tracking"
    request_track = requests.get(url, headers=global_headers(request))

    if request_track.status_code != 200:
        return render_error(request_track)

    request_corp = get_corporations_corporation_id(corp_id)
    if request_corp.status_code != 200:
        return render_error(request_corp)


    return render(request, "corporation/tracking.html", {
        "tracking": request_track.json(),
        "corporation_id": corp_id,
        "corporation_name": request_corp.json()["name"],
    })

@check_tokens(4)
def change_scopes(request, corp_id):
    """
    Changing corporation mandatory scopes
    """

    scopes = []
    for key in request.POST:
        if key in ESI_SCOPES:
            scopes.append(key)

    if len(scopes) > 0:
        data = "{\"mandatory_esi_scopes\": [\"" + "\",\"".join(scopes) + "\"]}"
    else:
        data = "{\"mandatory_esi_scopes\": []}"
    request_change = requests.put(GLOBAL_URL+f"/{corp_id}", headers=global_headers(request, {"Content-type":"application/json"}), data=data)
    if request_change.status_code != 200:
        return render_error(request_change)

    params = urlencode({"changed_scopes": "true"})
    return_url = reverse("corporation-sheet", args=[corp_id]) + "?" + params
    return redirect(return_url)
