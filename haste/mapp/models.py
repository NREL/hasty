from django.db import models

# Create your models here.


# class Mapper(models.Model):
class InferenceVersion(models.Model):
    version = models.CharField(max_length=20, null=False, blank=False, unique=True)

    def __str__(self):
        return self.version


class HaystackVersion(models.Model):
    version = models.CharField(max_length=20, null=False, blank=False, unique=True)

    def __str__(self):
        return self.version


class BrickVersion(models.Model):
    version = models.CharField(max_length=20, null=False, blank=False, unique=True)

    def __str__(self):
        return self.version


class HaystackMarkerTag(models.Model):
    tag = models.CharField(max_length=100, null=False, blank=False)
    version = models.ForeignKey(HaystackVersion, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        unique_together = ('tag', 'version',)


class BrickTag(models.Model):
    tag = models.CharField(max_length=100, null=False, blank=False)
    version = models.ForeignKey(BrickVersion, on_delete=models.CASCADE)
    namespace = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        unique_together = ('tag', 'version',)


class BrickPointType(models.Model):
    tags = models.ManyToManyField(BrickTag)
    brick_class = models.CharField(max_length=150, null=False, blank=False)
    version = models.ForeignKey(BrickVersion, on_delete=models.CASCADE)

    def __str__(self):
        return self.brick_class


class HaystackPointType(models.Model):
    marker_tags = models.ManyToManyField(HaystackMarkerTag)
    haystack_tagset = models.CharField(max_length=150, null=False, blank=False)
    version = models.ForeignKey(HaystackVersion, on_delete=models.CASCADE)

    def __str__(self):
        return self.haystack_tagset


class PointTypeMap(models.Model):
    inference_version = models.ForeignKey(InferenceVersion, on_delete=models.CASCADE)
    haystack_version = models.ForeignKey(HaystackVersion, on_delete=models.CASCADE)
    brick_version = models.ForeignKey(BrickVersion, on_delete=models.CASCADE)
    brick_point = models.ForeignKey(BrickPointType, on_delete=models.CASCADE, null=True, blank=False)
    haystack_point = models.ForeignKey(HaystackPointType, on_delete=models.CASCADE, null=True, blank=False)


class HaystackEquipmentType(models.Model):
    marker_tags = models.ManyToManyField(HaystackMarkerTag)
    haystack_tagset = models.CharField(max_length=150, null=False, blank=False)
    version = models.ForeignKey(HaystackVersion, on_delete=models.CASCADE)

    def __str__(self):
        return self.haystack_tagset


class BrickEquipmentType(models.Model):
    tags = models.ManyToManyField(BrickTag)
    brick_class = models.CharField(max_length=150, null=False, blank=False)
    version = models.ForeignKey(BrickVersion, on_delete=models.CASCADE)

    def __str__(self):
        return self.brick_class
