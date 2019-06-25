from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Ground(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    #longitude = models.DecimalField(max_digits= None, decimal_places=None)
    #latitute = models.DecimalField(max_digits= None, decimal_places=None)
    contact = models.IntegerField(default= 0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.IntegerField()
    ground = models.ForeignKey(Ground,on_delete=models.CASCADE)
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    reserved_date = models.DateField()


class Rating(models.Model):
    ground = models.ForeignKey(Ground,on_delete=models.CASCADE)
    rate = models.IntegerField(default=3)







