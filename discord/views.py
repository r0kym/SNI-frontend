from django.http import HttpResponse
from django.shortcuts import render

from utils import SNI_URL
from SNI.check import check_tokens
from SNI.error import render_error
from SNI.lib import global_headers

import requests

# Create your views here.

@check_tokens()
def home(request):
    """
    Home view of discord
    """

    url = SNI_URL + "discord/auth/start"

    request_auth_code = requests.post(url, headers=global_headers(request))

    if request_auth_code.status_code == 200:
        return render(request, 'discord/home.html', {
            "request_code": request_auth_code.json()
        })

    elif request_auth_code.status_code == 404:
        return render(request, 'discord/notactive.html')
    else:
        return render_error(request_auth_code)
