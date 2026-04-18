from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "pages/index.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
