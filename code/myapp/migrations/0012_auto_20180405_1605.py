# Generated by Django 2.0.1 on 2018-04-05 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20180405_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment_model',
            name='author',
        ),
        migrations.RemoveField(
            model_name='suggestion_model',
            name='author',
        ),
    ]