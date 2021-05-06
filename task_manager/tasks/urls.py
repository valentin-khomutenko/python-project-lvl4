from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('', views.ListTasks.as_view(), name='list_tasks'),
    path('create/', views.CreateTask.as_view(), name='create_task'),
    path('<int:pk>', views.TaskDetail.as_view(), name='task_detail'),
    path('<int:pk>/delete/', views.DeleteTask.as_view(), name='delete_task'),
    path('<int:pk>/update/', views.UpdateTask.as_view(), name='update_task'),
]
