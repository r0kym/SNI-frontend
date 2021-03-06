from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.defaults import bad_request
from django.urls import reverse
from urllib.parse import urlencode

import datetime
import requests

from utils import SNI_URL, SNI_DYNAMIC_TOKEN, SNI_TEMP_USER_TOKEN
from SNI.error import render_error
from SNI.check import check_tokens
from SNI.lib import global_headers, get_clearance_level


GLOBAL_URL = SNI_URL + "group"


@check_tokens()
def home(request):
    """
    Will display all the groups registered on the SNI
    """

    request_groups = requests.get(GLOBAL_URL, headers=global_headers(request))

    if request_groups.status_code != 200:
        return render_error(request_group)

    group_list = request_groups.json()
    print(group_list)
    return render(request, 'group/home.html', {
        "group_list": group_list,
        "new_group": request.GET.get("new_group"),
        "deleted_group": request.GET.get("del_group"),
        "new_member": request.GET.get("new_member"),
        "removed_member": request.GET.get("rem_member"),
        "clearance_level": get_clearance_level(request)
    })

@check_tokens()
def sheet(request, group_id):
    """
    Will display the main page for accessing group informations
    """

    url = f"{GLOBAL_URL}/{group_id}"

    request_group = requests.get(url, headers=global_headers(request))
    if request_group.status_code != 200:
        return render_error(request_group)

    request_group_json = request_group.json()
    if "root" in request_group_json["members"]:
      request_group_json["members"].remove("root")

    return render(request, 'group/sheet.html', {
        "group": request_group_json,
        "new_member": request.GET.get("new_member"),
        "removed_member": request.GET.get("rem_member"),
        "clearance_level": get_clearance_level(request)
    })

@check_tokens()
def new(request):
    """
    Display tools to create a new group
    """

    return render(request, 'group/new.html', {})

@check_tokens()
def create(request):
    """
    Create a new group
    This link should only be accessed by a redirection from group/new

    note: maybe use a post or something to make sure the group isn't created several times?
    """

    headers = global_headers(request)
    headers.update({"Content-type": "application/json"})

    data = "{\"group_name\":\"" + request.GET.get("name") + "\"}"

    request_create_group = requests.post(GLOBAL_URL, headers=headers, data=data)

    print(request_create_group)
    print(request_create_group.json())

    if request_create_group.status_code != 201:
        return render_error(request_create_group)

    return_url = reverse("group-home")
    params = urlencode({"new_group":request.GET.get("name")})
    url = f"{return_url}?{params}"

    return redirect(url)

@check_tokens()
def delete(request, group_id):
    """
    Deletes a group
    """

    url = f"{GLOBAL_URL}/{group_id}"

    request_group = requests.get(url, headers=global_headers(request))  # stores group params

    if request_group.status_code != 200:
        return render_error(request_group)

    request_delete_group = requests.delete(url, headers=global_headers(request))

    if request_delete_group.status_code != 200:
        return render_error(request_delete_group)

    params = urlencode({"del_group": request_group.json()["group_name"]})
    return_url = f"{reverse('group-home')}?{params}"

    return redirect(return_url)

@check_tokens()
def add_member(request, group_id):
    """
    Add an member to the group
    """

    url = f"{GLOBAL_URL}/{group_id}"

    headers = global_headers(request)
    headers.update({"Content-type": "application/json"})

    data = "{\"add_members\": [\"" + str(request.POST.get("member")) + "\"]}"

    request_new = requests.put(url, headers=headers, data=data)

    if request_new.status_code != 200:
        return render_error(request_new)

    print(request_new.status_code)
    print(request_new.json())

    params = urlencode({"new_member": request.POST.get("member")})
    return_url = reverse("group-home", args=[group_id]) + "?" + params

    return redirect(return_url)

@check_tokens()
def remove_member(request, group_id, member):
    """
    Removes an member from the group
    """

    url = f"{GLOBAL_URL}/{group_id}"

    headers = global_headers(request)
    headers.update({"Content-type": "application/json"})

    data = "{\"remove_members\": [\"" + str(member) + "\"]}"

    request_remove= requests.put(url, headers=headers, data=data)

    if request_remove.status_code != 200:
        return render_error(request_remove)

    print(request_remove.status_code)
    print(request_remove.json())

    params = urlencode({"rem_member": member})
    return_url = reverse("group-home", args=[group_id]) + "?" + params

    return redirect(return_url)
