# Generated by Django 2.0.1 on 2018-04-01 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_student_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student_model',
            name='avatar',
        ),
    ]
