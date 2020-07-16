from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN
from SNI.error import render_error

import datetime
import requests

def home(request):
  """
  Will start authentictaion to TeamSpeak
  """

  url = SNI_URL + "teamspeak/auth/start"
  headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
  }

  request_teamspeak_auth = requests.post(url, headers=headers)

  if request_teamspeak_auth.status_code != 200:
    return render_error(request_teamspeak_auth)


  teamspeak_auth = request_teamspeak_auth.json()

  return render(request, 'teamspeak/home.html', {"teamspeak_auth": teamspeak_auth})

def completed(request):
  """
  Will complete authentictaion to TeamSpeak
  """

  url = SNI_URL + "teamspeak/auth/complete"
  headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {SNI_TEMP_USER_TOKEN}"
  }

  request_teamspeak_auth = requests.post(url, headers=headers)

  if request_teamspeak_auth.status_code != 201:
    return render_error(request_teamspeak_auth)


  teamspeak_auth = request_teamspeak_auth.json()
  print(teamspeak_auth)

  return render(request, 'teamspeak/completed.html')
