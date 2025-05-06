from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-task/', views.add_task, name='add_task'),
    path('task/<int:pk>', views.task_details, name='task_details')
]