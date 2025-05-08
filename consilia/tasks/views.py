from datetime import datetime

from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm, SubtaskFormSet, SubtaskForm
from .models import Tasks, Subtasks


def index(request):
    to_do = Tasks.objects.filter(status=Tasks.Status.TODO)
    in_progress = Tasks.objects.filter(status=Tasks.Status.IN_PROGRESS)
    done = Tasks.objects.filter(status=Tasks.Status.DONE)
    date = datetime.today().strftime('%d.%m.%Y')
    return render(request, 'tasks/index.html', context={'to_do': to_do, 'in_progress': in_progress, 'done': done, 'date': date})


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        formset = SubtaskFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            task = form.save()
            subtasks = formset.save(commit=False)
            for subtask in subtasks:
                subtask.task = task
                subtask.save()
            return redirect('index')
    else:
        form = TaskForm()
        formset = SubtaskFormSet()
    return render(request, 'tasks/add_task.html', {'form': form, 'formset': formset})


def task_details(request, pk):
    task = Tasks.objects.get(pk=pk)
    subtasks = Subtasks.objects.filter(task=task.id)
    return render(request, 'tasks/task_details.html', context={'task': task, 'subtasks': subtasks})


def edit_task(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    SubtaskFormSet = inlineformset_factory(
        Tasks, Subtasks,
        form=SubtaskForm,
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        formset = SubtaskFormSet(request.POST, instance=task)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('task_details', pk=task.pk)

    else:
        form = TaskForm(instance=task)
        formset = SubtaskFormSet(instance=task)
    return render(request, 'tasks/add_task.html', {'form': form, 'task': task, 'formset': formset})


def delete_task(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    else:
        return render(request, 'tasks/delete_task.html', {'task': task})


