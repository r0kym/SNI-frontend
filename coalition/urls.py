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
    path('<str:coalition_id>/remove/<int:alliance_id>', views.remove_alliance, name='coalition-remove-alliance'),
    path('<str:coalition_id>/delete', views.delete, name='coalition-delete'),
    path('<str:coalition_id>/ticker', views.ticker, name='coalition-ticker'),
    path('<str:coalition_id>/scopes', views.scopes, name='coaliton-scopes'),
    path('<str:coalition_id>/scopes/all', views.scopes_all, name='coalition-scopes-all'),
    path('<str:coalition_id>/scopes/none', views.scopes_none, name='coalition-scopes-none'),
    path('<str:coalition_id>/tracking', views.tracking, name='coalition-tracking'),
]
