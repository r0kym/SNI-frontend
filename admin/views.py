"""
Admin app views
"""


from django.shortcuts import render

from SNI.check import check_tokens
from SNI.error import render_error
from utils import SNI_URL

import requests
from urllib.parse import urlencode


@check_tokens(10)
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

@check_tokens(10)
def submit(request):
    """
    Submits a job to the scheduler
    """

    callable_name = request.POST["callable_name"]
    url = SNI_URL + f"system/job/{callable_name}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {request.session['user_token']}"
    }

    request_submit = requests.post(url, headers=headers)

    if request_submit.status_code != 200:
        return render_error(request_submit)

    params = urlencode({'sub_job': callable_name})
    return_url = reverse("admin-home") + "?" + params

    return redirect(return_url)
