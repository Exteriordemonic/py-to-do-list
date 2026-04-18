from django.urls import path

from tasks.views import (
    TaskCreateView,
    TaskUpdateView,
    complete_task,
    undo_task,
)

urlpatterns = [
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("complete/<int:pk>/", complete_task, name="task-complete"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="task-update"),
    path("undo/<int:pk>/", undo_task, name="task-undo"),
]
