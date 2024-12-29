from django.db import models

# Create your models here.


class Currency(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
    

class article(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name