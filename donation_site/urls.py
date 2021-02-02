from django.urls import path, re_path
from donation_site import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name="about"),
    path('my_posts/', views.my_posts, name='my_posts'),
    re_path(r'^organization/(?P<pk>\d+)$', views.organization, name='organization'),
    re_path(r'^post/(?P<pk>\d+)$', views.post, name='post'),
]
