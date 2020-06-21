from utils import SNI_URL, SNI_DYNAMIC_TOKEN

from django.shortcuts import render
from django.http import HttpResponse

import requests


# Create your views here.

def home(request):
    # print(request.GET)   # access the get
    return render(request, 'home.html', {})

def auth(request):
    """Template page before there's an actual system in place"""

    headers = {"Authorization": f"Bearer {SNI_DYNAMIC_TOKEN}"}
    url = SNI_URL + "/token/use/from/dyn"
    r = requests.post(url, headers=headers)

    if r.status_code == "200":
        return HttpResponse("It worked \\o/")
    else:
        return HttpResponse("T'rahk messed up (as usual) go and blame him")
