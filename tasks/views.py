from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from tasks.forms import CreateTaskForm
from tasks.models import Task


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
