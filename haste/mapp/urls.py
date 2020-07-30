from django.urls import path

from . import views

urlpatterns = [
    path('', views.PointMappingView.as_view(), name='mapp.index'),
]
