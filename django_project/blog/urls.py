#from tempfile import template

#from django.contrib import admin
#from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
#from .views import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView



urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('login/', views.LoginView, name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]





