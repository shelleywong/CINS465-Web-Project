# Generated by Django 2.0.1 on 2018-03-04 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion', models.CharField(max_length=240)),
                ('author', models.CharField(blank=True, max_length=240, null=True)),
            ],
        ),
    ]
