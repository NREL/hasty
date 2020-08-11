from django.db import models

from mapp.models import HaystackVersion, HaystackPointType, HaystackEquipmentType


# Create your models here.
class HaystackEquipmentTemplate(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    version = models.ForeignKey(HaystackVersion, on_delete=models.CASCADE)
    equipment_type = models.ForeignKey(HaystackEquipmentType, on_delete=models.CASCADE)
    points = models.ManyToManyField(HaystackPointType)
