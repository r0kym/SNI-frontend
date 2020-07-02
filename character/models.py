from django.db import models

# Create your models here.


class CorporationName(models.Model):
    corporation_id = models.IntegerField()
    corporation_name = models.CharField(max_length=50)  # A corporation name has to contain at least four characters and no more than 50 characters. It may only contain letters, numbers, spaces, and dots (full stop or period).
