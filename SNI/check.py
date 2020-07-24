"""
Containns commands used to check user accesses to different pages
"""


from utils import SNI_URL

from django.shortcuts import redirect

import requests


def check_tokens(view, min_clearance=0):
    """
    Will check if there's a user token in the browser's cookies before executing the function and will redirect to the
    homepage if there's none

    min_clearance: minimal clearance needed to load the page.
    """

    def wrapper(request, *args, **kwargs):

        if (token := request.session.get("user_token")):

            if min_clearance != 0:
                url = SNI_URL + f"user/{request.session['user_id']}"
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {token}"
                }

                request_user = requests.get(url, headers=headers)

                if request_user.json()["clearance_level"] < min_clearance:
                    redirect('no-premission')

            return view(request, *args, **kwargs)
        else:
            return redirect("/")

    return wrapper
