from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('transactions', views.transactions),
    
]
