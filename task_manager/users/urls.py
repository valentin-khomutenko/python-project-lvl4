from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('users/create/', views.CreateUser.as_view(), name='create_user'),
    path('users/', views.ListUsers.as_view(), name='list_users'),
]
