# Generated by Django 5.1.2 on 2024-10-29 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0011_course_trainer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Trainer's name", max_length=100)),
                ('email', models.EmailField(help_text="Trainer's email address", max_length=254, unique=True)),
                ('specialization', models.CharField(help_text="Trainer's area of expertise", max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='trainer',
        ),
        migrations.CreateModel(
            name='CourseTrainerAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True, help_text='The date and time when the trainer was assigned')),
                ('course', models.ForeignKey(help_text='The course to which the trainer is assigned', on_delete=django.db.models.deletion.CASCADE, to='hr.course')),
                ('trainer', models.ForeignKey(help_text='The trainer assigned to the course', on_delete=django.db.models.deletion.CASCADE, to='hr.trainer')),
            ],
        ),
    ]
