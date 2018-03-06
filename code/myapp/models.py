from django.db import models
from django.utils import timezone

# Create your models here.

class Suggestion_Model(models.Model):
    suggestion = models.CharField(max_length=240)
    author = models.CharField(null=True, blank=True, max_length=240)

    def __str__(self):
        return "Suggestion by" + str(self.author) + ": " + str(self.suggestion)

# class Student(models.Model):
#     firstName = models.CharField(max_length=50)
#     lastName = models.CharField(max_length=50)
#     birthDate = models.DateField()


#class Book(models.Model):
    # title = models.CharField(max_length=255)
    # blurb = models.TextField(blank=True)
    # num_pages = models.IntegerField(blank=True)
    # available = models.BooleanField(default=True)
    #
    # def __str__(self):
    #     return self.title
