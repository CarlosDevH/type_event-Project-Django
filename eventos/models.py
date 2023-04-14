from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Event(models.Model):
    creator = models.ForeignKey(User, on_delete = models.DO_NOTHING, null = True, blank = True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    workload = models.IntegerField()
    logo = models.ImageField(upload_to = 'logo')

    #paletas de cores
    cor_principal = models.CharField(max_length = 7)
    cor_secundaria = models.CharField(max_length = 7)
    cor_fundo = models.CharField(max_length = 7)

    def __str__(self) -> str:
        return self.name