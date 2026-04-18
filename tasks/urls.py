from django.urls import path

from tasks.views import (
    TaskCreateView,
)

urlpatterns = [
    path("create/", TaskCreateView.as_view(), name="task-create"),
]
