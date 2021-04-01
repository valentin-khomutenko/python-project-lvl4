from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('statuses/', views.ListStatuses.as_view(), name='list_statuses'),
]
