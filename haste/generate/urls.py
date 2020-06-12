from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_site', views.CreateSite.as_view(), name='add_site'),
    path('site/<site_id>', views.Site.as_view(), name='site'),
    path('site/<site_id>/ahu/<ahu_id>', views.AirHandler.as_view(), name='site.ahu'),
]
