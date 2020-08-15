from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request
from django.urls import reverse

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN

from SNI.esi import post_universe_names, post_universe_ids, ESI_SCOPES
from SNI.error import render_error
from SNI.check import check_tokens
from SNI.lib import global_headers, get_clearance_level

import datetime
import requests
from urllib.parse import urlencode


GLOBAL_URL = SNI_URL + "coalition"


@check_tokens()
def home(request):
  """
  Will display all the coalitions registered on the SNI
  """

  request_coalitions = requests.get(GLOBAL_URL , headers=global_headers(request))


  if request_coalitions.status_code != 200:
    return render_error(request_coalitions)

  coalition_list = request_coalitions.json()
  coalition_dict = {}

  for coalition in coalition_list:
    request_coalition_details = requests.get(f"{GLOBAL_URL}/{coalition['coalition_id']}", headers=global_headers(request))

    if request_coalition_details.status_code != 200:
      return render_error(request_coalition_details)

    coalition_details = request_coalition_details.json()
    coalition_dict[coalition['coalition_id']] = coalition_details
    coalition_dict[coalition['coalition_id']]['members'] = len(coalition_details['member_alliances'] + coalition_details['member_corporations'])

  return render(request, 'coalition/home.html', {
    "coalition_list": coalition_dict,
    "new_coalition": request.GET.get("new_coa"),
    "deleted_coalition": request.GET.get("del_coa"),
    "clearance_level": get_clearance_level(request)
    })

@check_tokens()
def sheet(request, coalition_id):
    """
    Will display the main page for accessing coalition informations
    """

    url = f"{GLOBAL_URL}/{coalition_id}"

    request_coalition = requests.get(url, headers=global_headers(request))
    if request_coalition.status_code != 200:
        return render_error(request_coalition)

    return render(request, 'coalition/sheet.html', {
        "coalition": request_coalition.json(),
        "new_alliance": request.GET.get("new_ally"),
        "removed_corporation": request.GET.get("rem_corp"),
        "removed_alliance": request.GET.get("rem_ally"),
        "new_ticker": request.GET.get("new_ticker"),
        "not_found": request.GET.get("not_found"),
        "scopes": ESI_SCOPES,
        "clearance_level": get_clearance_level(request)
    })

@check_tokens(9)
def new(request):
    """
    Display tools to create a new coalition
    """

    return render(request, 'coalition/new.html', {})

@check_tokens(9)
def create(request):
    """
    Create a new coalition
    This link should only be accessed by a redirection from coalition/new

    note: maybe use a post or something to make sure the coalition isn't created several times?
    """

    headers = global_headers(request)
    headers.update({"Content-type": "application/json"})

    data = "{\"coalition_name\":\"" + request.GET.get("name") + "\",\"ticker\":\"" + request.GET.get("ticker") + "\"}"

    request_create_coalition = requests.post(GLOBAL_URL, headers=headers, data=data)

    if request_create_coalition.status_code != 201:
        return render_error(request_create_coalition)

    return redirect("coalition-sheet", coalition_id=request_create_coalition.json()["coalition_id"])

@check_tokens(9)
def delete(request, coalition_id):
    """
    Deletes a coaliton
    """

    url = f"{GLOBAL_URL}/{coalition_id}"

    request_coalition = requests.get(url, headers=global_headers(request))  # stores coalition params

    if request_coalition.status_code != 200:
        return render_error(request_coalition)

    request_delete_coalition = requests.delete(url, headers=global_headers(request))

    if request_delete_coalition.status_code != 200:
        return render_error(request_delete_coalition)

    params = urlencode({"del_coa": request_coalition.json()["coalition_name"]})
    return_url = f"{reverse('coalition-home')}?{params}"

    return redirect(return_url)

@check_tokens(9)
def add(request, coalition_id):
    """
    Add a new member to the coalition (alliance or corporation)
    """

    url = f"{GLOBAL_URL}/{coalition_id}"

    headers = global_headers(request)
    headers.update({"Content-type": "application/json"})

    request_member_id = post_universe_ids(request.POST.get("member"))
    if request_member_id.status_code != 200:
        return render_error(request_alliance_id)

    if "alliances" in request_member_id.json():
        t = "alliance"
        alliance_id = request_member_id.json()["alliances"][0]["id"]
        data = "{\"add_member_alliances\": [\"" + str(alliance_id) + "\"]}"
    elif "corporations" in request_member_id.json():
        t = "coproration"
        corporation_id = request_member_id.json()["corporations"][0]["id"]
        data = "{\"add_member_corporations\": [\"" + str(corporation_id) + "\"]}"
    else:
        params = urlencode({"not_found": request.POST.get("alliance")})
        return_url = reverse("coalition-sheet", args=[coalition_id]) + "?" + params
        return redirect(return_url)

    request_new = requests.put(url, headers=headers, data=data)

    if request_new.status_code == 404:  # case when the alliance isn't know by the backend yet
        if t == "alliance":
            request_fetch = requests.post(SNI_URL+f"alliance/{alliance_id}", headers=global_headers(request))
        else:
            request_fetch = requests.post(SNI_URL+f"corporation/{corporation_id}", headers=global_headers(request))
        if request_fetch.status_code != 200:
            return render_error(request_fetch)
        request_new = requests.put(url, headers=headers, data=data)  # tries again to add the alliance

    if request_new.status_code != 200:
        return render_error(request_new)

    params = urlencode({"new_member": request.POST.get("member")})
    return_url = reverse("coalition-sheet", args=[coalition_id]) + "?" + params

    return redirect(return_url)

@check_tokens(9)
def remove_alliance(request, coalition_id, alliance_id):
    """
    Removes an alliance from the coalition
    """

    url = f"{GLOBAL_URL}/{coalition_id}"

    headers = global_headers(request)
    headers.update({"Content-type": "application/json"})

    data = "{\"remove_member_alliances\": [\"" + str(alliance_id) + "\"]}"

    request_remove = requests.put(url, headers=headers, data=data)

    if request_remove.status_code != 200:
        return render_error(request_remove)

    request_alliance_name = post_universe_names(alliance_id)

    if request_alliance_name.status_code != 200:
        return render_error(request_alliance_name)

    alliance_name = request_alliance_name.json()[0]["name"]

    params = urlencode({"rem_ally": alliance_name})
    return_url = reverse("coalition-sheet", args=[coalition_id]) + "?" + params

    return redirect(return_url)

@check_tokens(9)
def remove_corporation(request, coalition_id, corporation_id):
    """
    Removes a corporation from the coalition
    """

    url = f"{GLOBAL_URL}/{coalition_id}"

    headers = global_headers(request)
    headers.update({"Content-type": "application/json"})

    data = "{\"remove_member_corporations\": [\"" + str(corporation_id) + "\"]}"

    request_remove = requests.put(url, headers=headers, data=data)

    if request_remove.status_code != 200:
        return render_error(request_remove)

    request_corporation_name = post_universe_names(corporation_id)

    if request_corporation_name.status_code != 200:
        return render_error(request_corporation_name)

    corproation_name = request_corporation_name.json()[0]["name"]

    params = urlencode({"rem_corp": corproation_name})
    return_url = reverse("coalition-sheet", args=[coalition_id]) + "?" + params

    return redirect(return_url)

@check_tokens(9)
def ticker(request, coalition_id):
    """
    Change a coalition ticker
    """

    url = f"{GLOBAL_URL}/{coalition_id}"

    headers = global_headers(request)
    headers.update({"Content-type": "application/json"})

    data = "{\"ticker\":\"" + request.POST.get("ticker") + "\"}"
    request_ticker = requests.put(url, headers=headers, data=data)

    if request_ticker.status_code != 200:
        return render_error(request_ticker)

    params = urlencode({"new_ticker": request.POST.get("ticker")})
    return_url = reverse("coalition-sheet", args=[coalition_id]) + "?" + params
    return redirect(return_url)

@check_tokens(9)
def scopes(request, coalition_id):
    """
    Update coalition required scopes with a specific set of scopes
    """

    scopes = []
    for key in request.POST:
        if key in ESI_SCOPES:
            scopes.append(key)

    url = f"{GLOBAL_URL}/{coalition_id}"

    headers = global_headers(request, {"Content-type": "application/json"})

    data = "{\"mandatory_esi_scopes\": [\"" + "\",\"".join(scopes) + "\"]}"

    request_change_scopes = requests.put(url, headers=headers, data=data)

    if request_change_scopes.status_code != 200:
        return render_error(request_change_scopes)

    params = urlencode({"changed_scopes": "true"})
    return_url = reverse("coalition-sheet", args=[coalition_id]) + "?" + params
    return redirect(return_url)

@check_tokens(9)
def scopes_all(request, coalition_id):
    """
    Update coalition required scopes with all scopes
    """

    headers = global_headers(request, {"Content-type": "application/json"})
    data = "{\"mandatory_esi_scopes\": [\"" + "\",\"".join(ESI_SCOPES) + "\"]}"
    request_change_scopes = requests.put(GLOBAL_URL+f"/{coalition_id}", headers=headers, data=data)
    if request_change_scopes.status_code != 200:
        return render_error(request_change_scopes)

    params = urlencode({"changed_scopes": "true"})
    return_url = reverse("coalition-sheet", args=[coalition_id]) + "?" + params
    return redirect(return_url)

@check_tokens(9)
def scopes_none(request, coalition_id):
    """
    Update coalition required scopes by removing them all
    """

    headers = global_headers(request, {"Content-type": "application/json"})
    data = "{\"mandatory_esi_scopes\": []}"
    request_change_scopes = requests.put(GLOBAL_URL+f"/{coalition_id}", headers=headers, data=data)
    if request_change_scopes.status_code != 200:
        return render_error(request_change_scopes)

    params = urlencode({"changed_scopes": "true"})
    return_url = reverse("coalition-sheet", args=[coalition_id]) + "?" + params
    return redirect(return_url)

@check_tokens(9)
def tracking(request, coalition_id):
    """
    Display the tracking of the coalition members
    """

    request_coa = requests.get(GLOBAL_URL+f"/{coalition_id}", headers=global_headers(request))
    if request_coa.status_code != 200:
        return render_error(request_coa)

    url = GLOBAL_URL + f"/{coalition_id}/tracking"
    request_track = requests.get(url, headers=global_headers(request))
    if request_track.status_code != 200:
        return render_error(request_track)

    return render(request, "coalition/tracking.html", {
        "coalition": request_coa.json(),
        "tracking": request_track.json(),
    })
