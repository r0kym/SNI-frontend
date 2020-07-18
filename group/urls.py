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
    path('<str:group_id>/add_member', views.add_member, name='group-add_member'),
    path('<str:group_id>/remove/<str:member>', views.remove_member, name='group-remove_member')
]
