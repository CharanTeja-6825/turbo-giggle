# Generated by Django 5.1.2 on 2024-11-01 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0015_remove_course_trainer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='created_at',
        ),
        migrations.AddField(
            model_name='course',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
