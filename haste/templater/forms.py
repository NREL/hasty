from django import forms
from . import models
from mapp.models import HaystackPointType, HaystackEquipmentType


class HaystackEquipmentTemplateForm(forms.ModelForm):
    equipment_type = forms.ModelChoiceField(queryset=HaystackEquipmentType.objects.order_by('haystack_tagset'))
    points = forms.ModelMultipleChoiceField(queryset=HaystackPointType.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.HaystackEquipmentTemplate
        fields = ('__all__')
