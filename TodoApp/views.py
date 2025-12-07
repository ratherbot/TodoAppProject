from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from TodoApp.forms import *
from TodoApp.models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'TodoApp/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        status = self.request.GET.get('status', 'all')

        if self.request.user.is_authenticated:
            queryset = Task.objects.filter(user=self.request.user)
        else:
            queryset = None

        if status == 'done':
            queryset = queryset.filter(is_done=True)
        elif status == 'not_done':
            queryset = queryset.filter(is_done=False)
        elif status == 'overdue':
            queryset = [task for task in queryset.filter(is_done=False) if task.is_overdue()]

        return queryset

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'TodoApp/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'TodoApp/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

class CreateTaskView(LoginRequiredMixin, CreateView):
    form_class = AddTaskForm
    template_name = 'TodoApp/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def about(request):
    return render(request, 'TodoApp/about.html')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def logout_user(request):
    logout(request)
    return redirect('login')