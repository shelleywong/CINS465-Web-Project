from django.urls import path, include

from . import views
from .forms import Login_Form
from django.contrib.auth import views as adminviews

urlpatterns = [
    path('', views.index),
    path('search/', views.search_view),
    path('about/', views.about_view),
    path('profile/', views.profile_view),
    path('profile/edit_profile/',views.edit_profile_view),
    path('profile/password/', views.change_password_view),
    path('message_board/', views.message_board_view),
    path('message_board_posts/', views.message_board_api),
    path('comment/<int:post_topic_id>/',views.comment_view),
    path('people/meet/',views.meet_view),
    path('people/roster/',views.roster_view),
    path('people/face_match/', views.face_match_view),
    path('people/students/', views.students_api),
    path('group/<slug:this_user>/',views.person_view, name='person'),
    path('chat/chatroom/', views.chatroom, name='chatroom'),
    path('login/', adminviews.login, {
        'template_name':'registration/login.html',
        'authentication_form':Login_Form
        }, name='login'
    ),
    path('logout/', adminviews.logout, {
        'next_page':'/'
    }),
    path('register/', views.register),

    # path('suggestion/', views.suggestion_view),
    # path('suggestions/', views.suggestion_api),
    # path('book/',views.book_view),
    # path('chat/chatroom/', views.chatroom, name='chatroom'),
    # path('chat/<slug:room_name>/', views.room, name='room'),
    #path('page<int:page_num>/',views.page),
]
