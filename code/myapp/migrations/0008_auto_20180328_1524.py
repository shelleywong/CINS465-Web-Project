# Generated by Django 2.0.1 on 2018-03-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20180327_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion_model',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]