from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('', views.ListLabels.as_view(), name='list_labels'),
    path('create/', views.CreateLabel.as_view(), name='create_label'),
    path('<int:pk>/delete/', views.DeleteLabel.as_view(), name='delete_label'),
    path('<int:pk>/update/', views.UpdateLabel.as_view(), name='update_label'),
]
