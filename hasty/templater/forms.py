from django import forms
from . import models
from mapp.models import HaystackPointType, HaystackEquipmentType, BrickPointType, BrickEquipmentType


class HaystackEquipmentTemplateForm(forms.ModelForm):
    equipment_type = forms.ModelChoiceField(
        queryset=HaystackEquipmentType.objects.order_by('haystack_tagset'))
    points = forms.ModelMultipleChoiceField(
        queryset=HaystackPointType.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.HaystackEquipmentTemplate
        fields = ('__all__')


class BrickEquipmentTemplateForm(forms.ModelForm):
    equipment_type = forms.ModelChoiceField(
        queryset=BrickEquipmentType.objects.order_by('brick_class'))
    points = forms.ModelMultipleChoiceField(
        queryset=BrickPointType.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.BrickEquipmentTemplate
        fields = ('__all__')


class HaystackFaultTemplateForm(forms.ModelForm):
    equipment_type = forms.ModelChoiceField(
        queryset=HaystackEquipmentType.objects.order_by('haystack_tagset'))
    points = forms.ModelMultipleChoiceField(
        queryset=HaystackPointType.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.HaystackFaultTemplate
        fields = ('__all__')


class BrickFaultTemplateForm(forms.ModelForm):
    equipment_type = forms.ModelChoiceField(
        queryset=BrickEquipmentType.objects.order_by('brick_class'))
    points = forms.ModelMultipleChoiceField(
        queryset=BrickPointType.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = models.BrickFaultTemplate
        fields = ('__all__')
