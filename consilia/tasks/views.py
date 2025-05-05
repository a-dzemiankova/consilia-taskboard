from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'tasks/index.html')


def add_task(request):
    return render(request, 'tasks/add_task.html')