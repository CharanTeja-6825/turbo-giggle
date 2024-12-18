# Generated by Django 5.1.3 on 2024-12-05 16:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_initial'),
        ('hr', '0021_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='hr.course')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('employee', 'course')},
            },
        ),
        migrations.DeleteModel(
            name='CourseEnrollment',
        ),
    ]
