from typing import List

from django.urls import path, URLPattern
from .views import CreateUser, Login

urlpatterns: List[URLPattern] = [
    path('users/create/', CreateUser.as_view(), name='create_user'),
    path('login/', Login.as_view(), name='login')
]
