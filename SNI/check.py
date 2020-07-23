"""
Containns commands used to check user accesses to different pages
"""

from django.shortcuts import redirect


def check_tokens(view):
    """
    Will check if there's a user token in the browser's cookies before executing the function and will redirect to the
    homepage if there's none
    """

    def wrapper(request, *args, **kwargs):

        if request.session.get("user_token"):
            return view(request, *args, **kwargs)
        else:
            return redirect("/")

    return wrapper
