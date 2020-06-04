from django import forms
from . import models


class SiteForm(forms.ModelForm):
    class Meta:
        model = models.Site
        fields = ('name', 'city', 'state',)
