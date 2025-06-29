from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    subject = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - Teacher"   

class ClassRoom(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    section = models.CharField(max_length=10, blank=True, null=True)  

    def __str__(self):
        return f"{self.name}{'-' + self.section if self.section else ''}"
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    classrooms = models.ManyToManyField(ClassRoom, related_name='subjects')

    def __str__(self):
        return self.name
    
class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=20)
    roll_number = models.CharField(max_length=10)
    grade = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, related_name='students')

    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Student"