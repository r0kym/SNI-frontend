import requests, json
from django.http import HttpResponse

def render_error(request):
    return HttpResponse(f"""<pre>ERROR {request.status_code}<br>{json.dumps(request.json(), indent=1)}</pre>""")