"""
Admin app views
"""


from django.shortcuts import render

from SNI.check import check_tokens
from SNI.error import render_error
from utils import SNI_URL

import requests


#@check_tokens(10)
def home(request):
    """
    Home view for the administration part
    """

    url = SNI_URL + "system/job"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }

    request_jobs = requests.get(url, headers=headers)

    if request_jobs.status_code != 200:
        return render_error(request_jobs)

    return render(request, 'admin/home.html', {
        "jobs": request_jobs.json(),
    })
