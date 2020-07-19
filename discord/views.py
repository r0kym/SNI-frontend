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

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {request.session['user_token']}"
    }

    request_auth_code = requests.post(url, headers=headers)

    if request_auth_code.status_code != 200:
        return HttpResponse(f"""
        ERROR {request_auth_code.status_code} <br>
        {request_auth_code.json()}""")

    return render(request, 'discord/home.html', {
        "request_code": request_auth_code.json()
    })
