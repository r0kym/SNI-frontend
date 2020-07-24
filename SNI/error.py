import requests, json
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied, SuspiciousOperation

def render_error(request):
    if request.status_code == 403:
        raise PermissionDenied
    else:
        return HttpResponse(f"""<pre>ERROR {request.status_code}<br>{json.dumps(request.json(), indent=1)}</pre>""")
