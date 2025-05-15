from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-task/', views.add_task, name='add_task'),
    path('task/<int:pk>', views.task_details, name='task_details'),
    path('task/edit/<int:pk>', views.edit_task, name='edit_task'),
    path('task/delete/<int:pk>', views.delete_task, name='delete_task'),
    path('tasks/<int:pk>/change_status/', views.change_status, name='change_status'),

]

