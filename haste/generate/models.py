from django.db import models

# Create your models here.
class Site(models.Model):
    # STATES = (
    #     ()
    # )
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=1)
