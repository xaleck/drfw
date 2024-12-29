from django.db import models

# Create your models here.


class Currency(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    

class Event(models.Model):
    user = models.CharField(max_length=250)
    currency = models.CharField(max_length=250)
    count = models.CharField(max_length=250)
    price = models.CharField(max_length=250)
    sum = models.CharField(max_length=250)
    type = models.CharField(max_length=250)

    def __str__(self):
        return self.sum