from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


from django.contrib.auth.models import User
from django.apps import apps
from hr.models import Course

class EmployeeCourse(models.Model):

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'course')

    def __str__(self):
        return f"{self.employee.username} - {self.course.course_name}"

