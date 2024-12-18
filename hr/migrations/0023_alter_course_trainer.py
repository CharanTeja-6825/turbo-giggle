# Generated by Django 5.1.4 on 2024-12-05 20:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0022_assignment_material'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='trainer',
            field=models.ForeignKey(limit_choices_to={'username__regex': '^\\\n    d{4}$'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
