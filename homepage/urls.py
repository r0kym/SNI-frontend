"""
URLconf of the homepage
"""


from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('auth/public', views.auth_public, name='auth-public'),
    path('auth/full', views.auth_full, name='auth-full'),
    path('callback/sni', views.sni_callback, name='sni_callback'),
    path('logout', views.logout, name='logout'),
]
