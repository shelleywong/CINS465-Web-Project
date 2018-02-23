from django.db import models

# Create your models here.

class Task(models.Model):
    def foo(self):
        return "bar"

#class Book(models.Model):
    # title = models.CharField(max_length=255)
    # blurb = models.TextField(blank=True)
    # num_pages = models.IntegerField(blank=True)
    # available = models.BooleanField(default=True)
    #
    # def __str__(self):
    #     return self.title
