from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request
from django.urls import reverse

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN
from SNI.esi import post_universe_names, post_universe_ids

import datetime
import requests
from urllib.parse import urlencode


def home(request):
  """
  Will display all the coalitions registered on the SNI
  """

  url = SNI_URL + "coalition"
  headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
  }

  request_coalitions = requests.get(url, headers=headers)

  if request_coalitions.status_code == 200:
    coalition_list = request_coalitions.json()
    print(coalition_list)
    coalition_dict = {}

    for coalition in coalition_list:
      request_coalition_details = requests.get(f"{url}/{coalition['coalition_id']}", headers=headers)

      if request_coalition_details.status_code == 200:
        coalition_details = request_coalition_details.json()
        coalition_dict[coalition['coalition_id']] = coalition_details
      else:
        return HttpResponse(f"""
        ERROR {request_coalition_details.status_code} <br>
        {request_coalition_details.json()}""")

    return render(request, 'coalition/home.html', {
        "coalition_list": coalition_dict,
        "new_coalition": request.GET.get("new_coa")
        })
  else:
    return HttpResponse(f"""
    ERROR {request_coalitions.status_code} <br>
    {request_coalitions.json()}""")

def sheet(request, coalition_id):
    """
    Will display the main page for accessing coalition informations
    """

    url = SNI_URL + f"coalition/{coalition_id}"
    headers = {
      "accept": "application/json",
      "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
    }

    request_coalition = requests.get(url, headers=headers)
    if request_coalition.status_code != 200:
      return HttpResponse(f"""
      ERROR {request_coalitions.status_code} <br>
      {request_coalitions.json()}""")

    print(request_coalition.json())

    if len(request_coalition.json()["members"]) != 0:
        coalition_members = [int(i) for  i in request_coalition.json()["members"]]
        coalition_members_names = post_universe_names(*coalition_members)

        if coalition_members_names.status_code != 200:
            return HttpResponse(f"""
            ERROR {coalition_members_names.status_code} <br>
            {coalition_members_names.json()}""")
        members_names = coalition_members_names.json()
    else:
        members_names = []


    return render(request, 'coalition/sheet.html', {
        "coalition": request_coalition.json(),
        "new_alliance": request.GET.get("new_ally"),
        "removed_alliance": request.GET.get("rem_ally"),
        "members_names": members_names

    })

def new(request):
    """
    Display tools to create a new coalition
    """

    return render(request, 'coalition/new.html', {})

def create(request):
    """
    Create a new coalition
    This link should only be accessed by a redirection from coalition/new

    note: maybe use a post or something to make sure the coalition isn't created several times?
    """

    url = SNI_URL + "coalition"

    headers = {
        "accept": "application/json",
        "Content-type": "application/json",
        "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
    }

    data = "{\"coalition_name\":\"" + request.GET.get("name") + "\",\"ticker\":\"" + request.GET.get("ticker") + "\"}"

    request_create_coalition = requests.post(url, headers=headers, data=data)

    print(request_create_coalition)
    print(request_create_coalition.json())

    if request_create_coalition.status_code != 201:
        return HttpResponse(f"""
        ERROR {request_create_coalition.status_code} <br>
        {request_create_coalition.json()}""")

    return_url = reverse("coalition-home")
    params = urlencode({"new_coa":request.GET.get("name")})
    url = f"{return_url}?{params}"

    return redirection(url)

def add(request, coalition_id):
    """
    Displays informations to add a new alliance to the coalition
    """

    return render(request, 'coalition/add.html', {})

def add_alliance(request, coalition_id):
    """
    Add an alliance to the coalition
    """

    url = SNI_URL + f"coalition/{coalition_id}"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
    }

    request_alliance_id = post_universe_ids(request.POST.get("name"))

    if request_alliance_id.status_code != 200:
        return HttpResponse(f"""
        ERROR {request_alliance_id.status_code} <br>
        {request_alliance_id.json()}""")

    data = "{\"add_members\": [\"" + str(request_alliance_id.json()["alliances"][0]["id"]) + "\"]}"

    request_new = requests.put(url, headers=headers, data=data)

    if request_new.status_code != 200:
        return HttpResponse(f"""
        ERROR {request_new.status_code} <br>
        {request_new.json()}""")

    print(request_new.status_code)
    print(request_new.json())

    params = urlencode({"new_ally": request.POST.get("name")})
    return_url = reverse("coalition-home") + coalition_id + "?" + params

    return redirect(return_url)

def remove_alliance(request, coalition_id, alliance_id):
    """
    Removes an alliance from the coalition
    """

    url = SNI_URL + f"coalition/{coalition_id}"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
    }

    request_alliance_name = post_universe_names(alliance_id)

    if request_alliance_name.status_code != 200:
        return HttpResponse(f"""
        ERROR {request_alliance_name.status_code} <br>
        {request_alliance_name.json()}""")

    alliance_name = request_alliance_name.json()[0]["name"]
    data = "{\"remove_members\": [\"" + alliance_name + "\"]}"

    request_remove= requests.put(url, headers=headers, data=data)

    if request_remove.status_code != 200:
        return HttpResponse(f"""
        ERROR {request_new.status_code} <br>
        {request_new.json()}""")

    print(request_remove.status_code)
    print(request_remove.json())

    params = urlencode({"rem_ally": alliance_name})
    return_url = reverse("coalition-home") + coalition_id + "?" + params

    return redirect(return_url)
