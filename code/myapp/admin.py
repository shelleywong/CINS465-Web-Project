from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Student_Model

# Register your models here.
from . import models

# Reference: https://docs.djangoproject.com/en/2.0/topics/auth/customizing/
class StudentInline(admin.StackedInline):
    model = Student_Model
    can_delete = False
    verbose_name_plural = 'student'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(models.Post_Model)
admin.site.register(models.Suggestion_Model)
admin.site.register(models.Comment_Model)
admin.site.register(models.Book)
