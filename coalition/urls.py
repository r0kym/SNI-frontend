"""
URLconf of the homepage
"""


from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('new', views.new, name='coalition-new'),
    path('create', views.create, name='coalition-create'),
    path('<str:coalition_id>', views.sheet, name='coalition-sheet'),
]
