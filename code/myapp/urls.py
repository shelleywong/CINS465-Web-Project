from django.urls import path, include

from . import views
from .forms import Login_Form
from django.contrib.auth import views as adminviews

urlpatterns = [
    path('', views.index),
    path('about/', views.about_view),
    path('profile/', views.profile_view),
    path('profile/edit_profile/',views.edit_profile_view),
    path('suggestion/', views.suggestion_view),
    path('suggestions/', views.suggestion_api),
    path('login/', adminviews.login, {
        'template_name':'registration/login.html',
        'authentication_form':Login_Form
    }, name='login'),
    path('logout/', adminviews.logout, {
        'next_page':'/'
    }),
    path('register/', views.register),

    path('book/',views.book_view),
    #path('page<int:page_num>/',views.page),
]
