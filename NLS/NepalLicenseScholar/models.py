from django.db import models
import uuid
import random


class BaseModel(models.Model):
  
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Contact(models.Model):
   
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=122)  
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=122)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name



class Category(models.Model):
  
    category_name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.category_name


DIFFICULTY_LEVELS = [
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard'),
]


class Question(BaseModel):
   
    category = models.ForeignKey(
        Category, 
        related_name='questions', 
        on_delete=models.CASCADE
    )
    question = models.CharField(max_length=100)
    marks = models.IntegerField(default=1)
    difficulty = models.CharField(
        max_length=100, 
        choices=DIFFICULTY_LEVELS, 
        default='Easy'
    )
    discrimination = models.CharField(max_length=100, default='h')
    guessing = models.CharField(max_length=100, null=True, blank=True, default='g')

    def __str__(self):
        return self.question

    def get_answer(self):
        
        answer_objs = list(Answer.objects.filter(question=self))
        random.shuffle(answer_objs)
        return [
            {'answer': answer_obj.answer, 'is_correct': answer_obj.is_correct}
            for answer_obj in answer_objs
        ]


class Answer(BaseModel):
   
    question = models.ForeignKey(
        Question, 
        related_name='answers', 
        on_delete=models.CASCADE
    )
    answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer
