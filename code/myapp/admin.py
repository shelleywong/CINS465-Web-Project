from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Suggestion_Model)
admin.site.register(models.Comment_Model)
admin.site.register(models.Book)
