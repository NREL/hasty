from django.db import models

from mapp.models import HaystackVersion, HaystackPointType, HaystackEquipmentType, BrickVersion, BrickEquipmentType, BrickPointType


class EquipmentTemplate(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)


class HaystackEquipmentTemplate(EquipmentTemplate):
    version = models.ForeignKey(HaystackVersion, on_delete=models.CASCADE)
    equipment_type = models.ForeignKey(
        HaystackEquipmentType,
        on_delete=models.CASCADE)
    points = models.ManyToManyField(HaystackPointType)


class BrickEquipmentTemplate(EquipmentTemplate):
    # For trying to get uniqueness across version, equipment_type, and points:
    # https://stackoverflow.com/questions/55196633/unique-together-and-m2m-field
    version = models.ForeignKey(BrickVersion, on_delete=models.CASCADE)
    equipment_type = models.ForeignKey(
        BrickEquipmentType, on_delete=models.CASCADE)
    points = models.ManyToManyField(BrickPointType)


class UseCaseTemplate(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)


class FaultTemplate(UseCaseTemplate):
    logic = models.TextField(max_length=1000, null=True, blank=True)


class HaystackFaultTemplate(FaultTemplate):
    version = models.ForeignKey(HaystackVersion, on_delete=models.CASCADE)
    equipment_type = models.ForeignKey(
        HaystackEquipmentType,
        on_delete=models.CASCADE)
    points = models.ManyToManyField(HaystackPointType)


class BrickFaultTemplate(FaultTemplate):
    version = models.ForeignKey(BrickVersion, on_delete=models.CASCADE)
    equipment_type = models.ForeignKey(
        BrickEquipmentType, on_delete=models.CASCADE)
    points = models.ManyToManyField(BrickPointType)
