from utils import SNI_URL, SNI_DYNAMIC_TOKEN

from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests


def home(request):
    # print(request.GET)   # access the get
    return render(request, 'home.html', {})

def auth(request):
    """
    Ask SNI for a login url with eve online and then redirect to it.
    """

    headers = {"Authorization": f"Bearer {SNI_DYNAMIC_TOKEN}"}
    json = {"scopes": ["publicData"]}
    url = SNI_URL + "token/use/from/dyn"
    r = requests.post(url, headers=headers, json=json)

    if r.status_code == 200:
        return redirect(r.json()["login_url"])
    else:
        return HttpResponse(f"""T'rahk messed up (as usual) go and blame him pls <br>
        <b>error code: {r.status_code} </b><br>
        error message: {r.json()}""")

def sni_callback(request):
    """
    Handles the request when the SNI send back the informations and redirect to the character page of
    the character that just logged in.
    """

    post_dic = request.POST

    request.session["character_id"] = post_dic["character_id"]
    request.session["user_token"] = post_dic["user_token"]

    return redirect(f"/character/{post_dic['character_id']}")
