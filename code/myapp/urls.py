from django.urls import path

from . import views

urlpatterns = [
    path('',views.index),
    path('suggestion/',views.suggestion_view),
    path('suggestions/', views.suggestion_api),
    path('login/',views.login_view),
    path('book/',views.book_view),
    #path('page<int:page_num>/',views.page),
]
