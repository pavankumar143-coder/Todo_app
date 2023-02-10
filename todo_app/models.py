from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.username
    

class Todo(models.Model):
    owner = models.ForeignKey( User, on_delete=models.CASCADE,null=True, blank=True,default=True)
    task = models.CharField(max_length=255)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

