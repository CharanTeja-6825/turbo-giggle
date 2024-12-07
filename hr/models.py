from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    duration = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50, unique=True)
    progress = models.IntegerField(default=0)
    description = models.TextField()
    trainer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'username__regex': r'^\d{4}$'},
    )

    def __str__(self):
        return self.course_name



class Material(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='materials/')  # This will store files in the 'materials/' directory
    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)  # Related to the Course model

    def __str__(self):
        return self.title


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    course = models.ForeignKey('Course', related_name='assignments', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# models.py
from django.db import models

class TrainingInquiry(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    company_name = models.CharField(max_length=255, blank=True)
    participants = models.PositiveIntegerField()
    message = models.TextField()

    def __str__(self):
        return self.full_name


from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)  # Trainer who received the feedback
    rating = models.IntegerField()  # Rating from 1 to 5
    comments = models.TextField()  # Detailed comments

    def __str__(self):
        return f"Feedback from {self.trainer.username} (Rating: {self.rating})"

