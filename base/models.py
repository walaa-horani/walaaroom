from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True,unique=True)
    
    bio = models.TextField(null=True)
    avatar= models.ImageField(null=True,upload_to='images/',blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('home')      


class Topic(models.Model):
   name = models.CharField(max_length=200)

   def __str__(self):
      return self.name



class Room(models.Model):
  host =  models.ForeignKey(User,on_delete=models.CASCADE)
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null= True)  

  name = models.CharField(max_length=200)
  description = models.TextField(null=True,blank=True)
  participants= models.ManyToManyField(User,related_name='participants',blank=True)
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)


  class Meta:
       ordering = ['-updated','-created']

  def __str__(self):
      return self.name


class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)    
    body =  models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]