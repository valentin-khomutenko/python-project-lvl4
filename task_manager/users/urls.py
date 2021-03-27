from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('users/create/', views.CreateUser.as_view(), name='create_user'),
    path('users/<int:pk>/delete/', views.DeleteUser.as_view(), name='delete_user'),
    path('users/<int:pk>/update/', views.UpdateUser.as_view(), name='update_user'),
    path('users/', views.ListUsers.as_view(), name='list_users'),
]
