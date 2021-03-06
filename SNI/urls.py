"""SNI URL Configuration

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

from django.urls import include, path

handeler404 = "homepage.views.not_found"
urlpatterns = [
    path('admin/', include('admin.urls')),
    path('', include('homepage.urls')),
    path('character/', include('character.urls')),
    path('corporation/', include('corporation.urls')),
    path('alliance/', include('alliance.urls')),
    path('coalition/', include('coalition.urls')),
    path('group/', include('group.urls')),
    path('teamspeak/', include('teamspeak.urls')),
    path('discord/', include('discord.urls')),
]
