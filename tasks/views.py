from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from tasks.forms import CreateTaskForm, CreateTagForm
from tasks.models import Task, Tag
from django.shortcuts import render


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("tasks:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("tasks:index")

    def get_queryset(self):
        return (
            Task.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("tags")
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "pages/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return (
            Task.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("tags")
        )


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:index")

    def get_queryset(self):
        return (
            Task.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("tags")
        )


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    context_object_name = "tags"

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).select_related(
            "user"
        )


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = CreateTagForm
    success_url = reverse_lazy("tasks:index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = CreateTagForm
    success_url = reverse_lazy("tasks:tag-list")

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).select_related(
            "user"
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy("tasks:tag-list")

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user).select_related(
            "user"
        )


@login_required
def complete_task(request, pk):
    if request.method == "POST":
        task = Task.objects.get(pk=pk, user=request.user)
        task.completed = True
        task.save()
        return redirect(reverse_lazy("tasks:index"))


@login_required
def undo_task(request, pk):
    if request.method == "POST":
        task = Task.objects.get(pk=pk, user=request.user)
        task.completed = False
        task.save()
        return redirect(reverse_lazy("tasks:index"))


@login_required
def search_tasks(request):
    query = request.GET.get("q")
    tasks = (
        Task.objects.filter(user=request.user, content__icontains=query)
        .select_related("user")
        .prefetch_related("tags")
    )
    return render(request, "pages/index.html", {"tasks": tasks})
