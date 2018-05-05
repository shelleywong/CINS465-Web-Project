from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #url(r'^$', views.index, name='index'),
    #url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    path('chat/<slug:room_name>/', views.room, name='room'),
]
