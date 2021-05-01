from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('statuses/', views.ListStatuses.as_view(), name='list_statuses'),
    path('statuses/create/', views.CreateStatus.as_view(), name='create_status'),
    path('statuses/<int:pk>/delete/', views.DeleteStatus.as_view(), name='delete_status'),
    path('statuses/<int:pk>/update/', views.UpdateStatus.as_view(), name='update_status'),
]
