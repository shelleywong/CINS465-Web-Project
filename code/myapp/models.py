from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models.aggregates import Count
from random import randint

# Create your models here.
class Chat_Model(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    message = models.TextField()
    message_html = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.message

class Post_Model(models.Model):
    subject = models.CharField(max_length=240)
    details = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.subject

class Post_Comment_Model(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post_topic = models.ForeignKey(Post_Model, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

# class UsersManager(models.Manager):
#     def random(self):
#         count = self.aggregate(count=Count('id'))['count']
#         random_index = randint(0, count - 1)
#         return self.all()[random_index]

#reference: https://docs.djangoproject.com/en/2.0/topics/auth/customizing/
#default image ref: https://stackoverflow.com/questions/13090505/render-default-image-django?rq=1
class Student_Model(models.Model):
    # objects = UsersManager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    image = models.ImageField(
        max_length=144,
        upload_to='uploads/%Y/%m/%d',
        blank=True,
        default='uploads/2018/04/17/default_profile_pic.jpg',
    )
    image_description = models.CharField(max_length=240, blank=True)

    def profilepic_or_default(self, default_path='uploads/2018/04/17/default_profile_pic.jpg'):
        if self.image:
            return self.image
        return default_path
#
# @receiver(post_save, sender=User)
# def Create_Student_Model(sender, instance, created, **kwargs):
#     if created:
#         Student_Model.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def Save_Student_Model(sender, instance, **kwargs):
#     instance.profile.save()

class Suggestion_Model(models.Model):
    suggestion = models.CharField(max_length=240)
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE
    # )
    #created_on = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "Suggestion: " + str(self.suggestion)

class Comment_Model(models.Model):
    comment = models.CharField(max_length=240)
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE
    # )
    #created_on = models.DateTimeField(auto_now_add=True, blank=True)
    suggestion = models.ForeignKey(Suggestion_Model, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

#reference: https://docs.djangoproject.com/en/2.0/topics/auth/customizing/
# class Student_Model(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     interests = models.TextField(blank=True)
#     image = models.ImageField(
#         max_length=144,
#         upload_to='uploads/%Y/%m/%d'
#     )
#     image_description = models.CharField(max_length=240)

# @receiver(post_save, sender=User)
# def Create_Student_Model(sender, instance, created, **kwargs):
#     if created:
#         Student_Model.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def Save_Student_Model(sender, instance, **kwargs):
#     instance.student_model.save()

# class Professor_Model(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     interests = models.TextField()
#     avatar = models.ImageField()
#     #permission to create group?

# class Student(models.Model):
#     firstName = models.CharField(max_length=50)
#     lastName = models.CharField(max_length=50)
#     birthDate = models.DateField()

#Practice model
#reference: https://www.youtube.com/watch?v=45J88cjmoQI (user: Katie Cunningham)
class Book(models.Model):
    title = models.CharField(max_length=255)
    blurb = models.TextField(blank=True)
    num_pages = models.IntegerField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
