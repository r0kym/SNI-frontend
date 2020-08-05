"""
URLconf of the homepage
"""


from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('auth/public', views.auth_public, name='auth-public'),
    path('auth/full', views.auth_full, name='auth-full'),
    path('callback/sni', views.sni_callback, name='sni_callback'),
    path('logout', views.logout, name='logout'),
    path('403', views.no_perm, name='no-permission'),
    path('404', views.not_found, name='not-found'),
]
