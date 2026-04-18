from django.urls import path

from tasks.views import (
    TaskCreateView,
    complete_task,
    undo_task,
)

urlpatterns = [
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("complete/<int:pk>/", complete_task, name="task-complete"),
    path("undo/<int:pk>/", undo_task, name="task-undo"),
]
