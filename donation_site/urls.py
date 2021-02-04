from django.urls import path, re_path
from donation_site import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name="about"),
    path('my_posts/', views.my_posts, name='my_posts'),
    re_path(r'^organization/(?P<pk>\d+)$', views.organization, name='organization'),
    re_path(r'^post/(?P<pk>\d+)$', views.post, name='post'),
    path('new_post/', views.create_post, name='create_post'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('registration/', views.registration_page, name='registration_page'),
]
