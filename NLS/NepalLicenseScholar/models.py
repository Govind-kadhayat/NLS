from django.db import models
import uuid


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)                 
  
    class Meta:
      abstract = True




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
    

class Category(models.Model):
   category_name = models.CharField(max_length=100)
  
  
  
class Question(BaseModel):
   Category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
   question = models.CharField(max_length=100)
   marks = models.IntegerField(default=5)


class Answer(BaseModel):
    question = models.ForeignKey(Question,related_name='question_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)