import json
from datetime import datetime

from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import TaskForm, SubtaskForm
from .models import Tasks, Subtasks


def get_data():
    to_do = Tasks.objects.filter(status=Tasks.Status.TODO)
    in_progress = Tasks.objects.filter(status=Tasks.Status.IN_PROGRESS)
    done = Tasks.objects.filter(status=Tasks.Status.DONE)
    date = datetime.today().strftime('%d.%m.%Y')
    data = {'to_do': to_do, 'in_progress': in_progress, 'done': done, 'date': date}
    return data


def page_not_found(request, exception):
    try:
        return render(request, 'tasks/404.html')
    except Exception as e:
        return HttpResponse(f'Ошибка в обработчике 404: {e}', status=500)


def index(request):
    return render(request, 'tasks/index.html', context=get_data())


def add_task(request):
    SubtaskFormSet = inlineformset_factory(
        Tasks, Subtasks,
        form=SubtaskForm,
        extra=0,
        can_delete=False
    )
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # ещё не сохраняем сабтаски
            formset = SubtaskFormSet(request.POST, instance=task)
            if formset.is_valid():
                task.save()  # сохраняем только после того, как formset валиден
                subtasks = formset.save(commit=False)
                for subtask in subtasks:
                    subtask.task = task
                    subtask.save()
                return redirect('index')
            else:
                print('formset errors:', formset.errors)
        else:
            formset = SubtaskFormSet(request.POST)  # для повторного отображения с ошибками
            print('form errors:', form.errors)
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
            print('something is wrong')
            print(f"form:{form.errors}, formset:{formset.errors}")

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


@csrf_exempt
def change_status(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = data.get('status')
        task = get_object_or_404(Tasks, pk=pk)
        task.status = new_status
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

