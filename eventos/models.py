from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    workload = models.IntegerField()
    logo = models.ImageField