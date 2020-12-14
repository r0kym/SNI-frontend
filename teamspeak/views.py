from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN
from SNI.error import render_error
from SNI.check import check_tokens
from SNI.lib import global_headers

import datetime
import requests

GLOBAL_URL = SNI_URL + "teamspeak"

@check_tokens()
def home(request):
    """
    Will start authentictaion to TeamSpeak
    """

    url = GLOBAL_URL + "/auth/start"

    request_teamspeak_auth = requests.post(url, headers=global_headers(request))

    if request_teamspeak_auth.status_code != 200:
        return render_error(request_teamspeak_auth)


    teamspeak_auth = request_teamspeak_auth.json()

    return render(request, 'teamspeak/home.html', {"teamspeak_auth": teamspeak_auth})

@check_tokens()
def completed(request):
    """
    Will complete authentictaion to TeamSpeak
    """

    url = GLOBAL_URL + "/auth/complete"

    request_teamspeak_auth = requests.post(url, headers=global_headers(request))

    if request_teamspeak_auth.status_code == 404:
        try:
            detail = request.json()["detail"]
        except KeyError:
            pass
        else:
            if detail == "Could not find corresponding teamspeak client":
                return render(request, "teamspek/notfound.html")

    if request_teamspeak_auth.status_code != 201:
        return render_error(request_teamspeak_auth)

    return render(request, 'teamspeak/completed.html')
