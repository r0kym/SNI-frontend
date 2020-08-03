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

]
