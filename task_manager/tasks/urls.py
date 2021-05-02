from typing import List
from django.urls import path, URLPattern
from django_filters.views import FilterView  # type: ignore
from . import filters
from . import views

urlpatterns: List[URLPattern] = [
    path('tasks/', FilterView.as_view(filterset_class=filters.TaskFilter,
         template_name='tasks/list.html'), name='list_tasks'),
    path('tasks/create/', views.CreateTask.as_view(), name='create_task'),
    path('tasks/<int:pk>/delete/', views.DeleteTask.as_view(), name='delete_task'),
    path('tasks/<int:pk>/update/', views.UpdateTask.as_view(), name='update_task'),
]
