from django.db import models

# Create your models here.
class User(models.Model):
    ip_address = models.GenericIPAddressField()
    times_visited = models.IntegerField(default=0)
