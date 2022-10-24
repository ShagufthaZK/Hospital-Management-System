from django.db import models

# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=122,blank=True,null=True)
    email=models.CharField(max_length=122,blank=True,null=True)
    
    
    def __str__(self):
        return self.name
    