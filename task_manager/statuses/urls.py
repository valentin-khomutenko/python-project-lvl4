from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('statuses/', views.ListStatuses.as_view(), name='list_statuses'),
    path('statuses/create/', views.CreateStatus.as_view(), name='create_status'),
]
