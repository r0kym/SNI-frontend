from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN

import datetime
import requests

def home(request):
    """
    Will display all the characters registered on the SNI
    """

    url = SNI_URL + "group"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
    }

    request_groups = requests.get(url, headers=headers)

    if request_groups.status_code == 200:
        group_list = request_groups.json()

        if "root" in group_list:
            group_list.remove("root")

        return render(request, 'group/home.html', {"group_list": group_list})
    else:
        return HttpResponse(f"""
        ERROR {request_groups.status_code} <br>
        {request_groups.json()}""")