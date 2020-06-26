from django.db import models

# Create your models here.


class CorporationName(models.Model):
    corporation_id = models.IntegerField()
    corporation_name = models.CharField(max_length=50)  # what's a corporation name max length?
