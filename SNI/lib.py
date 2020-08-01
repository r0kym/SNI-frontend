
from utils import SNI_URL
from SNI.error import render_error

import requests

def global_headers(request):
    """Give the headers that can be used everywhere here"""

    return {
        "accept": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }

def get_clearance_level(request):
    """Return the clearance level for curent user"""
    url = SNI_URL + f"user/{request.session['user_id']}"

    request_user = requests.get(url, headers=global_headers(request))

    if request_user.status_code != 200:
        return render_error(request_user)

    return request_user.json()["clearance_level"]