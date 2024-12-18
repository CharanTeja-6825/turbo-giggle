# Generated by Django 5.1.3 on 2024-12-06 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0023_alter_course_trainer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporateTrainingInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=15)),
                ('company_name', models.CharField(max_length=100)),
                ('participants', models.PositiveIntegerField()),
                ('message', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
