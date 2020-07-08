"""
URLconf of the homepage
"""


from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='coalition-home'),
    path('new', views.new, name='coalition-new'),
    path('create', views.create, name='coalition-create'),
    path('<str:coalition_id>', views.sheet, name='coalition-sheet'),
    path('<str:coalition_id>/add', views.add, name='coalition-add'),
    path('<str:coalition_id>/add/alliance', views.add_alliance, name='coalition-add-alliance'),
]
