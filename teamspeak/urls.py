"""
URLconf of the homepage
"""


from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='teamspeak-home'),
    path('completed', views.completed, name='teamspeak-completed')
]
