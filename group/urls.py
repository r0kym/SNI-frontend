"""
URLconf of the homepage
"""


from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='group-home'),
    path('new', views.new, name='group-new'),
    path('create', views.create, name='group-create'),
    path('<str:group_id>', views.sheet, name='group-sheet'),
    path('<str:group_id>/delete', views.delete, name='group-delete'),
]
