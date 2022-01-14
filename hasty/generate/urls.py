from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.ListSites.as_view(),
        name='index'),
    path(
        'create_site/',
        views.CreateSite.as_view(),
        name='create-site'),
    path(
        'create_from_template/',
        views.CreateFromTemplate.as_view(),
        name='create-from-template'),
    path(
        'site/<site_id>',
        views.SiteDetail.as_view(),
        name='site-detail'),
    path(
        'site/<site_id>/ahu/<ahu_id>',
        views.AirHandler.as_view(),
        name='site.ahu'),
    path(
        'data_view/<site_id>',
        views.data_view,
        name='data_view')]
