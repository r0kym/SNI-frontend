"""
URLconf of the homepage
"""


from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('auth', views.auth, name='auth'),
    path('callback/sni', views.sni_callback, name='sni_callback'),
]
