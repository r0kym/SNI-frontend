"""
Containns commands used to check user accesses to different pages
"""


from utils import SNI_URL

from django.shortcuts import redirect

import requests
from functools import wraps


def check_tokens(min_clearance=0):
    """
    Will check if there's a user token in the browser's cookies before executing the function and will redirect to the
    homepage if there's none

    min_clearance: minimal clearance needed to load the page.
    """
    def decorator(view):
        @wraps(view)
        def inner(request, *args, **kwargs):
            if (token := request.session.get("user_token")):
                if min_clearance != 0:
                    url = SNI_URL + f"user/{request.session['user_id']}"
                    headers = {
                        "accept": "application/json",
                        "Authorization": f"Bearer {token}"
                    }

                    request_user = requests.get(url, headers=headers)

                    if request_user.json()["clearance_level"] < min_clearance:
                        return redirect('no-premission')
                return view(request, *args, **kwargs)
            return redirect("/")
        return inner
    return decorator
