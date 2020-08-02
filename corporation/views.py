from django.shortcuts import render
from django.http import HttpResponse

from SNI.check import check_tokens
from SNI.error import render_error
from SNI.esi import post_universe_names
from SNI.lib import global_headers
from utils import SNI_URL

import requests


GLOBAL_URL = SNI_URL + "corporation"

@check_tokens(1)
def home(request):
    """
    Corporation home
    """

    request_corp = requests.get(GLOBAL_URL, headers=global_headers(request))
    if request_corp.status_code != 200:
        render_error(request_corp)

    return render(request, "corporation/home.html", {
        "corporations": request_corp.json(),
    })

@check_tokens(1)
def sheet(request, corp_id):
    """
    Information sheet on a corporation
    """
    return HttpResponse("Corp sheet")

@check_tokens(1)
def tracking(request, corp_id):
    """
    Tracking of the corp membres tokens
    """
    url = GLOBAL_URL + f"/{corp_id}/tracking"
    request_track = requests.get(url, headers=global_headers(request))

    if request_track.status_code != 200:
        return render_error(request_track)

    return render(request, "corporation/tracking.html", {
        "tracking": request_track.json(),
    })
