from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='templater.index'),
    path('equipment/haystack', views.HaystackCreateEquipmentTemplateView.as_view(), name='templater.haystack.create_equipment_template'),
    path('equipment/brick', views.BrickCreateEquipmentTemplateView.as_view(), name='templater.brick.create_equipment_template'),
    # path('create/fault', views.Index.as_view(), name='templater.create_fault_template'),
    # path('create/select_points', views.SelectPointsView.as_view(), name='templater.select_points')
]
