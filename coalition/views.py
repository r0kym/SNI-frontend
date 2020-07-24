from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request
from django.urls import reverse

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN

from SNI.esi import post_universe_names, post_universe_ids, ESI_SCOPES
from SNI.error import render_error
from SNI.check import check_tokens

import datetime
import requests
from urllib.parse import urlencode


@check_tokens()
def home(request):
  """
  Will display all the coalitions registered on the SNI
  """

  url = SNI_URL + "coalition"
  headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {request.session.get('user_token')}"
  }

  request_coalitions = requests.get(url, headers=headers)


  if request_coalitions.status_code != 200:
    return render_error(request_coalitions)

  coalition_list = request_coalitions.json()
  print(coalition_list)
  coalition_dict = {}

  for coalition in coalition_list:
    request_coalition_details = requests.get(f"{url}/{coalition['coalition_id']}", headers=headers)

    if request_coalition_details.status_code != 200:
      return render_error(request_coalition_details)

    coalition_details = request_coalition_details.json()
    coalition_dict[coalition['coalition_id']] = coalition_details

  return render(request, 'coalition/home.html', {
    "coalition_list": coalition_dict,
    "new_coalition": request.GET.get("new_coa"),
    "deleted_coalition": request.GET.get("del_coa")
    })

@check_tokens()
def sheet(request, coalition_id):
    """
    Will display the main page for accessing coalition informations
    """

    url = SNI_URL + f"coalition/{coalition_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }

    request_coalition = requests.get(url, headers=headers)
    if request_coalition.status_code != 200:
        return render_error(request_coalition)

    print(request_coalition.json())

    if len(request_coalition.json()["members"]) != 0:
        coalition_members = [int(i) for  i in request_coalition.json()["members"]]
        coalition_members_names = post_universe_names(*coalition_members)

        if coalition_members_names.status_code != 200:
            return render_error(coalition_members_names)

        members_names = coalition_members_names.json()
    else:
        members_names = []

    return render(request, 'coalition/sheet.html', {
        "coalition": request_coalition.json(),
        "new_alliance": request.GET.get("new_ally"),
        "removed_alliance": request.GET.get("rem_ally"),
        "new_ticker": request.GET.get("new_ticker"),
        "members_names": members_names,
        "scopes": ESI_SCOPES,
    })

@check_tokens()
def new(request):
    """
    Display tools to create a new coalition
    """

    return render(request, 'coalition/new.html', {})

@check_tokens()
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
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }

    data = "{\"coalition_name\":\"" + request.GET.get("name") + "\",\"ticker\":\"" + request.GET.get("ticker") + "\"}"

    request_create_coalition = requests.post(url, headers=headers, data=data)

    print(request_create_coalition)
    print(request_create_coalition.json())

    if request_create_coalition.status_code != 201:
        return render_error(request_create_coalition)

    return_url = reverse("coalition-home")
    params = urlencode({"new_coa":request.GET.get("name")})
    url = f"{return_url}?{params}"

    return redirect(url)

@check_tokens()
def delete(request, coalition_id):
    """
    Deletes a coaliton
    """

    url = SNI_URL + f"coalition/{coalition_id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }

    request_coalition = requests.get(url, headers=headers)  # stores coalition params

    if request_coalition.status_code != 200:
        return render_error(request_coalition)

    request_delete_coalition = requests.delete(url, headers=headers)

    if request_delete_coalition.status_code != 200:
        return render_error(request_delete_coalition)

    params = urlencode({"del_coa": request_coalition.json()["coalition_name"]})
    return_url = f"{reverse('coalition-home')}?{params}"

    return redirect(return_url)

@check_tokens()
def add(request, coalition_id):
    """
    Add an alliance to the coalition
    """

    url = SNI_URL + f"coalition/{coalition_id}"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }

    request_alliance_id = post_universe_ids(request.POST.get("alliance"))

    if request_alliance_id.status_code != 200:
        return render_error(request_alliance_id)

    data = "{\"add_members\": [\"" + str(request_alliance_id.json()["alliances"][0]["id"]) + "\"]}"

    request_new = requests.put(url, headers=headers, data=data)

    if request_new.status_code != 200:
        return render_error(request_new)

    print(request_new.status_code)
    print(request_new.json())

    params = urlencode({"new_ally": request.POST.get("alliance")})
    return_url = reverse("coalition-home") + coalition_id + "?" + params

    return redirect(return_url)

@check_tokens()
def remove_alliance(request, coalition_id, alliance_id):
    """
    Removes an alliance from the coalition
    """

    url = SNI_URL + f"coalition/{coalition_id}"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }

    data = "{\"remove_members\": [\"" + str(alliance_id) + "\"]}"

    request_remove= requests.put(url, headers=headers, data=data)

    if request_remove.status_code != 200:
        return render_error(request_remove)

    print(request_remove.status_code)
    print(request_remove.json())

    request_alliance_name = post_universe_names(alliance_id)

    if request_alliance_name.status_code != 200:
        return render_error(request_alliance_name)

    alliance_name = request_alliance_name.json()[0]["name"]

    params = urlencode({"rem_ally": alliance_name})
    return_url = reverse("coalition-home") + coalition_id + "?" + params

    return redirect(return_url)

@check_tokens()
def ticker(request, coalition_id):
    """
    Change a coalition ticker
    """

    url = SNI_URL + f"coalition/{coalition_id}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }

    data = "{\"ticker\":\"" + request.POST.get("ticker") + "\"}"
    request_ticker = requests.put(url, headers=headers, data=data)

    if request_ticker.status_code != 200:
        return render_error(request_ticker)

    params = urlencode({"new_ticker": request.POST.get("ticker")})
    return_url = reverse("coalition-home") + coalition_id + "?" + params
    return redirect(return_url)

@check_tokens()
def scopes(request, coalition_id):
    """
    Update coalition required scopes
    """

    scopes = []
    for key in request.POST:
        if key in ESI_SCOPES:
            scopes.append(key)

    url = SNI_URL + f"coalition/{coalition_id}"
    headers = {
        "accpet": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }
    data = "{\"mandatory_esi_scopes\": [\"" + "\",\"".join(scopes) + "\"]}"

    request_change_scopes = requests.put(url, headers=headers, data=data)

    if request_change_scopes.status_code != 200:
        return HttpResponse(f"""
        ERROR {request_change_scopes.status_code} <br>
        {request_change_scopes.json()}""")

    params = urlencode({"changed_scopes": "true"})
    return_url = reverse("coalition-home") + coalition_id + "?" + params
    return redirect(return_url)
