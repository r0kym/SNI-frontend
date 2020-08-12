from utils import SNI_URL, SNI_DYNAMIC_TOKEN
from SNI.esi import ESI_SCOPES
from SNI.error import render_error
from SNI.lib import global_headers

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader

import requests


def home(request):

    if (user_token := request.session.get("user_token")):

        headers = {"Authorization": f"Bearer {user_token}"}
        url = SNI_URL + "token"
        request_token = requests.get(url, headers=headers)

        if request_token.status_code != 200:
            return render_error(request_token)

        return redirect(reverse("character-sheet", args=[request_token.json()["owner_character_id"]]))

    return render(request, 'home.html', {
        "scopes": ESI_SCOPES,
    })

def auth(request):
    """
    Ask SNI for a login url with eve online with a specific set of scopes and then redirect to it.
    """

    headers = {"Authorization": f"Bearer {SNI_DYNAMIC_TOKEN}"}
    json = {"scopes": [scope for scope in request.POST if scope in ESI_SCOPES]}
    r = requests.post(SNI_URL+"token/use/from/dyn", headers=headers, json=json)

    if r.status_code != 200:
        return render_error(r)

    response = redirect(r.json()["login_url"])
    response.set_cookie("state_code", r.json()["state_code"], max_age=300)  # the login must be made in 5 minutes
    return response

def auth_public(request):
    """
    Ask SNI for a login url with eve online with `PublicData` as scope and then redirect to it.
    """

    headers = {"Authorization": f"Bearer {SNI_DYNAMIC_TOKEN}"}
    json = {"scopes": ["publicData"]}
    url = SNI_URL + "token/use/from/dyn"
    r = requests.post(url, headers=headers, json=json)

    if r.status_code != 200:
        return render_error(r)

    response = redirect(r.json()["login_url"])
    response.set_cookie("state_code", r.json()["state_code"], max_age=300)  # the login must be made in 5 minutes
    return response

def auth_full(request):
    """
    Ask SNI for a login url with eve online with all possible scopes and then redirect to it.
    """

    headers = {"Authorization": f"Bearer {SNI_DYNAMIC_TOKEN}"}
    json = {"scopes": ESI_SCOPES}
    url = SNI_URL + "token/use/from/dyn"
    r = requests.post(url, headers=headers, json=json)

    if r.status_code != 200:
        return render_error(r)

    response = redirect(r.json()["login_url"])
    response.set_cookie("state_code", r.json()["state_code"], max_age=300)  # the login must be made in 5 minutes
    return response

def auth_invite(request):
    """
    Retrives a state code, deduct scopes from it and ask for a login url with the specific scopes
    """

    esi_scopes = ESI_SCOPES
    esi_scopes.sort()
    code = request.POST.get("code")
    hex_scopes = int(code.split(":")[0], 16)

    # stolen from https://github.com/altaris/seat-navy-issue/blob/master/sni/esi/scope.py
    scopes = set()
    index = 0
    for scope in esi_scopes:
        if hex_scopes & (2 ** index) > 0:
            scopes.add(scope)
        index += 1

    headers = {"Authorization": f"Bearer {SNI_DYNAMIC_TOKEN}"}
    json = {"scopes": list(scopes), "state_code": code}
    url = SNI_URL + "token/use/from/dyn"
    r = requests.post(url, headers=headers, json=json)

    if r.status_code != 200:
        return render_error(r)

    response = redirect(r.json()["login_url"])
    response.set_cookie("state_code", r.json()["state_code"], max_age=300)  # the login must be made in 5 minutes
    return response

def sni_callback(request):
    """
    Handles the request when the SNI send back the informations and redirect to the character page of
    the character that just logged in.
    """

    get_dic = request.GET

    if request.COOKIES["state_code"] == get_dic["state_code"]:

        request.session["user_token"] = get_dic["user_token"]

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {get_dic['user_token']}"
        }
        request_token = requests.get(SNI_URL+"token", headers=headers)

        if request_token.status_code != 200:
            return render_error(request_token)
        print(request_token.json())
        request.session["user_id"] = request_token.json()["owner"]["character_id"]

        return redirect(f"/character/{request_token.json()['owner']['character_id']}")

    else:
        redirect("/")

def logout(request):
    """
    Will delete the current session and redirect toward the home page
    """
    request.session.flush()
    return redirect('/')

def no_perm(request):
    """
    General view when a user is trying something he shouldn't be able to do
    """
    return render(request, "403.html")

def not_found(request, exception):
    """
    General view when a user is trying to get an element not found
    """
    return render(request, "404.html")
