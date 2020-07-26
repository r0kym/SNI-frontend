import requests, json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied, SuspiciousOperation

def render_error(request):
    if request.status_code == 403:
        raise PermissionDenied
    elif request.status_code == 401:
        try:
            return redirect("logout")
        except KeyError:
            pass

        # response.delete_cookie('user_token')
        return redirect("/")
    else:
        return HttpResponse(f"""<pre>ERROR {request.status_code}<br>{json.dumps(request.json(), indent=1)}</pre>""")
