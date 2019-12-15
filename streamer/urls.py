from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'streamer'
urlpatterns = [
    path('', views.index, name='index'),
    path('watch/<watch_id>', views.video, name='watch'),
    path('edit/<watch_id>', views.editVideo, name='edit_video'),
    path('channel/<channel_id>', views.channel, name='channel'),
    path('upload/', views.uploadVideo, name='upload'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='streamer/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('history/', views.history, name='history'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('like/', views.like, name='like'),
    path('dislike/', views.dislike, name='dislike'),
    path('comment/', views.comment, name='comment'),
]