from django.db import models

from mapp.models import HaystackVersion, HaystackPointType, HaystackEquipmentType


# Create your models here.
class HaystackEquipmentTemplate(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    version = models.ForeignKey(HaystackVersion, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, null=True, blank=True)
    equipment_type = models.ForeignKey(HaystackEquipmentType, on_delete=models.CASCADE)
    points = models.ManyToManyField(HaystackPointType)

# For trying to get uniqueness across version, equipment_type, and points:
# https://stackoverflow.com/questions/55196633/unique-together-and-m2m-field
