from utils import SNI_URL, SNI_DYNAMIC_TOKEN
from SNI.esi import ESI_SCOPES

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from SNI.error import render_error

import requests


def home(request):

    if (user_token := request.session.get("user_token")):

        headers = {"Authorization": f"Bearer {user_token}"}
        url = SNI_URL + "token"
        request_token = requests.get(url, headers=headers)

        if request_token.status_code != 200:
            return render_error(request_token)

        return redirect(reverse("character-sheet", args=[request_token.json()["owner_character_id"]]))

    return render(request, 'home.html', {})

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

        request.session["user_id"] = request_token.json()["owner_character_id"]

        return redirect(f"/character/{request_token.json()['owner_character_id']}")

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

def not_found(request):
    """
    General view when a user is trying to get an element not found
    """
    return render(request, "404.html")
