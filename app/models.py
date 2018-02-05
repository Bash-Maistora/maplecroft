from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2, null=True)
    longitude = models.IntegerField(null=True)
    latitude = models.IntegerField(null=True)
