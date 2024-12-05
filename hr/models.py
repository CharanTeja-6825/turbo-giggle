from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'username__regex': r'^\d{4}$'})
    def __str__(self):
        return self.course_name
