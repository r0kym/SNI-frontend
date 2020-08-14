"""Characters URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:character_id>', views.sheet, name='character-sheet'),
    path('<int:character_id>/sni', views.sni, name='character-sni'),
    path('<int:character_id>/assets', views.assets, name='character-assets'),
    path('<int:character_id>/contracts', views.contracts, name='character-contracts'),
    path('<int:character_id>/contracts/<int:contract_id>', views.contracts_details, name='character-contracts-details'),
    path('<int:character_id>/locations', views.locations, name='character-locations'),
    path('<int:character_id>/mails', views.mails, name='character-mails'),
    path('<int:character_id>/skills', views.skills, name='character-skills'),
    path('<int:character_id>/wallet/journal', views.wallet_journal, name='character-wallet-journal'),
    path('<int:character_id>/wallet/transactions', views.wallet_transactions, name='character-wallet-transactions'),
]
