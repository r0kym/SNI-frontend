
def global_headers(request):
    """Give the headers that can be used everywhere here"""

    return {
        "accept": "application/json",
        "Authorization": f"Bearer {request.session.get('user_token')}"
    }
