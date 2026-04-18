from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from tasks.forms import CreateTaskForm
from tasks.models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "pages/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@login_required
def complete_task(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    task.completed = True
    task.save()
    return redirect(reverse_lazy("index"))


@login_required
def undo_task(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    task.completed = False
    task.save()
    return redirect(reverse_lazy("index"))
