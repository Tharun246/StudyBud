from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class topic(models.Model): 
    name=models.CharField(max_length=30)

    def __str__(self): 
        
        return self.name

class Room(models.Model): 
    topic=models.ForeignKey(topic,on_delete=models.SET_NULL,null=True,blank=True)
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=30)
    description=models.TextField(max_length=100,blank=True,null=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True,null=True)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        
        return self.name 

    class Meta: 
        
        ordering=['-created','updated']

class Message(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.SET_NULL,null=True)
    body=models.TextField(max_length=100,blank=True,null=True)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True)
    

    def __str__(self): 
        return self.body[0:50]
    
    class Meta: 
        ordering=['-created']

