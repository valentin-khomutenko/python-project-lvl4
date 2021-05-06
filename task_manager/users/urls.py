from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('create/', views.CreateUser.as_view(), name='create_user'),
    path('<int:pk>/delete/', views.DeleteUser.as_view(), name='delete_user'),
    path('<int:pk>/update/', views.UpdateUser.as_view(), name='update_user'),
    path('', views.ListUsers.as_view(), name='list_users'),
]
