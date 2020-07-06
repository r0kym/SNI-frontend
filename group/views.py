from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN

import datetime
import requests

global_url = SNI_URL + "group"

global_headers = {
  "accept": "application/json",
  "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
}

def home(request):
  """
  Will display all the groups registered on the SNI
  """

  if request.GET.get('delete', None):
    url=f"{global_url}/{request.GET.get('delete')}"
    request_groups = requests.delete(url, headers=global_headers)
    if request_groups.status_code == 200:
      print("group deleted")
    else:
      return HttpResponse(f"""
      ERROR {request_group_details.status_code} <br>
      {request_group_details.json()}""")

  request_groups = requests.get(global_url, headers=global_headers)

  if request_groups.status_code == 200:
    group_list = request_groups.json()

    group_dict = {}

    for group in group_list:
      request_group_details = requests.get(f"{global_url}/{group['group_id']}", headers=global_headers)

      if request_group_details.status_code == 200:
        group_details = request_group_details.json()
        group_dict[group['group_id']] = group_details
      else:
        return HttpResponse(f"""
        ERROR {request_group_details.status_code} <br>
        {request_group_details.json()}""")

    return render(request, 'group/home.html', {"group_list": group_dict})
  else:
    return HttpResponse(f"""
    ERROR {request_groups.status_code} <br>
    {request_groups.json()}""")

def sheet(request, group_id):
    """
    Will display the main page for accessing group informations
    """

    url = f"{global_url}/{group_id}"

    request_group = requests.get(url, headers=global_headers)
    if request_group.status_code != 200:
      return HttpResponse(f"""
      ERROR {request_groups.status_code} <br>
      {request_groups.json()}""")

    print(request_group.json())

    return render(request, 'group/sheet.html', {
        "group": request_group.json()
    })