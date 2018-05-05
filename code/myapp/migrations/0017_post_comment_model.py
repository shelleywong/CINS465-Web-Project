# Generated by Django 2.0.1 on 2018-04-08 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0016_auto_20180407_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post_Comment_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post_topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Post_Model')),
            ],
        ),
    ]
