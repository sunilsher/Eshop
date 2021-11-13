from django.contrib import admin
from django.urls import path
from .views import index, Signup, Login

urlpatterns = [
    path('', index, name='homepage'),
    path('signup', Signup.as_view()),
    path('login', Login.as_view())
]
