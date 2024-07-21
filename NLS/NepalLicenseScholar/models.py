from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone= models.CharField(max_length=10)
    address= models.CharField(max_length=122)
    desc= models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name
class Signup(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone= models.CharField(max_length=10)
    address= models.CharField(max_length=122)
    password = models.CharField(max_length=112)
    date = models.DateField()

    def __str__(self):
        return self.name