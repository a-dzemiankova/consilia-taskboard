from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm
from .models import Tasks


def index(request):
    to_do = Tasks.objects.filter(status=Tasks.Status.TODO)
    in_progress = Tasks.objects.filter(status=Tasks.Status.IN_PROGRESS)
    done = Tasks.objects.filter(status=Tasks.Status.DONE)
    return render(request, 'tasks/index.html', context={'to_do': to_do, 'in_progress': in_progress, 'done': done})


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})


def task_details(request, pk):
    task = Tasks.objects.get(pk=pk)
    return render(request, 'tasks/task_details.html', context={'task': task})


def edit_task(request, pk):
    task = get_object_or_404(Tasks, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})
