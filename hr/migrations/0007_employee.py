# Generated by Django 5.1.2 on 2024-10-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0006_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('user_id', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Employees',
            },
        ),
    ]
