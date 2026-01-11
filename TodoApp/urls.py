from django.urls import path
from . import views
from .views import RegisterUser, logout_user, LoginUser, about, TaskListView, CreateTaskView, ShowTask, \
    TaskToggleDoneView, TaskDeleteView

urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('addtask/', CreateTaskView.as_view(), name='add_task'),
    path('task/<slug:task_slug>/', ShowTask.as_view(), name='task'),
    path('task/<slug:task_slug>/toggle/', TaskToggleDoneView.as_view(), name='task_toggle'),
    path('task/<slug:task_slug>/delete/', TaskDeleteView.as_view(), name='task_delete')
]