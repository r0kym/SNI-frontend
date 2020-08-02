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
]
