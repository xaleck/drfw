from django.db import models
from django.utils import timezone

# Create your models here.


class Currency(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    

class Event(models.Model):
    user = models.CharField(max_length=250)
    datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    currency = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.DecimalField(max_digits=10, decimal_places=2) 
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=250)

    def __str__(self):
        return self.sum