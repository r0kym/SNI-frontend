from django.http import HttpResponse
from django.shortcuts import render

from utils import SNI_URL

import requests

# Create your views here.

def home(request):
    """
    Home view of discord
    """

    url = SNI_URL + "discord/auth/start"

    try:
        token = request.session["user_token"]
    except KeyError:
        return render(request, 'discord/home.html', {"error": "Error when reading user token"})

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    request_auth_code = requests.post(url, headers=headers)

    if request_auth_code.status_code != 200:
        return HttpResponse(f"""
        ERROR {request_auth_code.status_code} <br>
        {request_auth_code.json()}""")

    return render(request, 'discord/home.html', {
        "request_code": request_auth_code.json()
    })
