from utils import SNI_URL, SNI_DYNAMIC_TOKEN
from SNI.esi import ESI_SCOPES

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

import requests


def home(request):

    if (user_token := request.session.get("user_token")):

        headers = {"Authorization": f"Bearer {user_token}"}
        url = SNI_URL + "token"
        request_token = requests.get(url, headers=headers)

        if request_token.status_code != 200:
            return HttpResponse(f"""
            ERROR {request_token.status_code} <br>
            {request_token.json()}""")

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

    if r.status_code == 200:
        response = redirect(r.json()["login_url"])
        response.set_cookie("status_code", r.json()["status_code"], max_age=300)  # the login must be made in 5 minutes
        return response
    else:
        return HttpResponse(f"""T'rahk messed up (as usual) go and blame him pls <br>
        <b>error code: {r.status_code} </b><br>
        error message: {r.json()}""")

def auth_full(request):
    """
    Ask SNI for a login url with eve online with all possible scopes and then redirect to it.
    """

    headers = {"Authorization": f"Bearer {SNI_DYNAMIC_TOKEN}"}
    json = {"scopes": ESI_SCOPES}
    url = SNI_URL + "token/use/from/dyn"
    r = requests.post(url, headers=headers, json=json)

    if r.status_code == 200:
        response = redirect(r.json()["login_url"])
        response.set_cookie("status_code", r.json()["status_code"], max_age=300)  # the login must be made in 5 minutes
        return response
    else:
        return HttpResponse(f"""T'rahk messed up (as usual) go and blame him pls <br>
        <b>error code: {r.status_code} </b><br>
        error message: {r.json()}""")

def sni_callback(request):
    """
    Handles the request when the SNI send back the informations and redirect to the character page of
    the character that just logged in.
    """

    get_dic = request.GET

    if request.COOKIES["status_code"] == get_dic["status_code"]:

        request.session["character_id"] = post_dic["character_id"]
        request.session["user_token"] = post_dic["user_token"]

        return redirect(f"/character/{post_dic['character_id']}")

    else:
        redirect("/")
