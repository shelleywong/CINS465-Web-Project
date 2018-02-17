from django.urls import path

from . import views

urlpatterns = [
    path('',views.index),
    #path('', views.head_display, name="head_display"),
    #path('page<int:page_num>/',views.page),
]
