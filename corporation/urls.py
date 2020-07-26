"""
Corporation URLconf
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='corporation-home'),
    path('<int:corp_id>/', views.sheet, name='corporation-sheet'),
]
