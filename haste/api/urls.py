from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='api.index'),
    path('sites', views.GetSites.as_view(), name='api.sites'),
    path('haystack/site/<site_id>', views.GenerateHaystack.as_view(), name="api.haystack.site"),
    path('haystack/download/<site_id>', views.GenerateHaystackFile.as_view(), name="api.haystack.download")
]
