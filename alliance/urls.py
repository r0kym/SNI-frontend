"""
Alliance URLconf
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='alliance-home'),
    path('<int:ally_id>/', views.sheet, name='alliance-sheet'),
    path('<int:ally_id>/tracking', views.tracking, name='alliance-tracking'),
    path('<int:ally_id>/scopes', views.change_scopes, name='alliance-change-scopes'),
    path('<int:ally_id>/scopes/all', views.change_scopes_all, name='alliance-change-scopes-all'),
    path('<int:ally_id>/scopes/none', views.change_scopes_none, name='alliance-change-scopes-none'),

]
