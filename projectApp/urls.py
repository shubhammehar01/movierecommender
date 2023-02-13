from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
   
    path('home',views.home,name='home'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('signin',views.signin,name='signin'),
    path('signout', views.signout, name='signout'),
    path('signup',views.signup,name='signup'),
]
