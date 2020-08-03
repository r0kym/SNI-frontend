"""
Corporation URLconf
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='corporation-home'),
    path('<int:corp_id>/', views.sheet, name='corporation-sheet'),
    path('<int:corp_id>/tracking', views.tracking, name='corporation-tracking'),
    path('<int:corp_id>/scopes', views.change_scopes, name='corpoation-change-scopes'),
    path('<int:corp_id>/scopes/all', views.change_scopes_all, name='corporation-change-scopes-all'),
    path('<int:corp_id>/scopes/none', views.change_scopes_none, name='corporation-change-scopes-none'),
]
