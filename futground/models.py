from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Ground(models.Model):
    name = models.CharField(max_length=1000)
    location = models.CharField(max_length=1000)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    contact = models.IntegerField(default= 0)
    price = models.IntegerField(default=1500)
    photo = models.ImageField(max_length=255,upload_to='futground/media',blank=True,null=True)
    #photo1 = models.ImageField()
    #photo2 = models.ImageField()

    def __str__(self):
        return self.name

    class Meta:
        ordering=['name']
class Reservation(models.Model):
    user = models.IntegerField()
    ground = models.ForeignKey(Ground,on_delete=models.CASCADE)
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    reserved_date = models.DateField()

    class Meta:
        ordering = ["reserved_date","starting_time","ending_time"]

    def __str__(self):
        return  str(self.reserved_date)


class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ground = models.ForeignKey(Ground,on_delete=models.CASCADE)
    rate = models.IntegerField(blank=True)
    avg_rating= models.FloatField(default=0.0,blank=True)
    num_rate = models.IntegerField(default=0,blank=True)

    def __str__(self):
          return str(self.user)+ "--" + str(self.ground) +"--"+ str(self.rate) + " -- " +str(self.avg_rating) +"--"+ str(self.num_rate)



