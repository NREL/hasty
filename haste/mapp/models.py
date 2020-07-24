from django.db import models

# Create your models here.


class Mapper(models.Model):
    BRICK_VERSIONS = (
        ('V1.1', 'V1.1'),
    )
    HAYSTACK_VERSIONS = (
        ('V3.9.9', '3.9.9'),
    )
    brick_version = models.CharField(max_length=20, choices=BRICK_VERSIONS)
    haystack_version = models.CharField(max_length=20, choices=HAYSTACK_VERSIONS)


class PointMapping(models.Model):
    brick_class = models.CharField(max_length=150, null=True, blank=True, default=None)
    haystack_tagset = models.CharField(max_length=150, null=True, blank=True, default=None)
    parent_map = models.ForeignKey(Mapper, on_delete=models.CASCADE)
