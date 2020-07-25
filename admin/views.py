"""
Admin app views
"""

from django.shortcuts import render

from utils import SNI_URL
from SNI.check import check_tokens
from SNI.error import render_error
from SNI.lib import global_headers

import requests
from urllib.parse import urlencode

GLOBAL_URL = SNI_URL + "system/job"

@check_tokens(10)
def home(request):
    """
    Home view for the administration part
    """

    request_jobs = requests.get(GLOBAL_URL, headers=global_headers(request))

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
    url = f"{GLOBAL_URL}/{callable_name}"

    request_submit = requests.post(url, headers=global_headers(request))

    if request_submit.status_code != 200:
        return render_error(request_submit)

    params = urlencode({'sub_job': callable_name})
    return_url = reverse("admin-home") + "?" + params

    return redirect(return_url)
