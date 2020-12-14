"""
URLconf of the homepage
"""


from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='teampseak-home'),
    path('completed', views.completed, name='teampseak-completed')
]
