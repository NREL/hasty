from django.urls import path

from . import views

urlpatterns = [
    path(
        '',
        views.Index.as_view(),
        name='templater.index'),
    path(
        'equipment/haystack',
        views.HaystackCreateEquipmentTemplateView.as_view(),
        name='templater.haystack.create_equipment_template'),
    path(
        'equipment/brick',
        views.BrickCreateEquipmentTemplateView.as_view(),
        name='templater.brick.create_equipment_template'),
    path(
        'fault/haystack',
        views.HaystackCreateFaultTemplateView.as_view(),
        name='templater.haystack.create_fault_template'),
    path(
        'fault/brick',
        views.BrickCreateFaultTemplateView.as_view(),
        name='templater.brick.create_fault_template'),
]
