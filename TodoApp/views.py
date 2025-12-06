from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import ListView

from TodoApp.models import Task


# Create your views here.
def index(request):
    tasks = Task.objects.all()
    return render(request, 'TodoApp/index.html', {'tasks': tasks})


def about(request):
    return render(request, 'TodoApp/about.html')

class TaskHome(ListView):
    model = Task

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')