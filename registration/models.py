from django.contrib.auth.models import AbstractUser
from django.db import models


class School_Info(models.Model):
    school_id = models.IntegerField(primary_key=True)
    school_name = models.CharField(max_length=100, unique=True)
    school_address = models.TextField()

    def __str__(self):
        return self.school_name


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    school_info = models.ForeignKey(School_Info, on_delete=models.CASCADE, default=None, null=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=3)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subject = models.CharField(max_length=20)
