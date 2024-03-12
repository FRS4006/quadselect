"""multipost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from logic.views import login_view, user_profile, one, deleteallps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('user_profile/', user_profile, name='user_profile'),
    path('user_profile/one', one, name='user_profile_one'),
    path('user_profile/deleteallps', deleteallps, name='user_profile_deleteallps'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', login_view, name='login_view'),
]