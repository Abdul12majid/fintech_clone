from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('wallets', views.wallets),
    path('send', views.send),
    path('login', views.login_user),
    path('register', views.register),
    
]
