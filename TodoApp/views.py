from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from TodoApp.forms import *
from TodoApp.models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'TodoApp/index.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        status = self.request.GET.get('status', 'all')

        if self.request.user.is_authenticated:
            queryset = Task.objects.filter(user=self.request.user)
        else:
            queryset = Task.objects.none()

        if status == 'done':
            queryset = queryset.filter(is_done=True)
        elif status == 'not_done':
            queryset = queryset.filter(is_done=False)
        elif status == 'overdue':
            queryset = queryset.filter(is_done=False, deadline__lt=timezone.now())

        return queryset

class TaskToggleDoneView(View):
    def post(self, request, task_slug):
        task = get_object_or_404(Task, slug=task_slug, user=request.user)
        task.is_done = not task.is_done
        task.save(update_fields=["is_done"])
        return redirect('home')

class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, task_slug):
        task = get_object_or_404(Task, slug=task_slug, user=request.user)
        task.delete()
        return redirect('home')

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

class ShowTask(DetailView):
    model = Task
    template_name = 'TodoApp/task.html'
    slug_url_kwarg = 'task_slug'
    context_object_name = 'task'

def about(request):
    return render(request, 'TodoApp/about.html')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def logout_user(request):
    logout(request)
    return redirect('login')