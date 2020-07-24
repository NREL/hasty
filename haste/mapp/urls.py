from django.urls import path

from . import views

urlpatterns = [
    path('', views.mapp_index, name='mapp.index'),
]
