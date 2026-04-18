from django.urls import path

from tasks.views import (
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    complete_task,
    undo_task,
    TagListView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    search_tasks,
)

urlpatterns = [
    path("create/", TaskCreateView.as_view(), name="task-create"),
    path("complete/<int:pk>/", complete_task, name="task-complete"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="task-update"),
    path("undo/<int:pk>/", undo_task, name="task-undo"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="task-delete"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("tags/create/", TagCreateView.as_view(), name="tag-create"),
    path("tags/update/<int:pk>/", TagUpdateView.as_view(), name="tag-update"),
    path("tags/delete/<int:pk>/", TagDeleteView.as_view(), name="tag-delete"),
    path("search/", search_tasks, name="task-search"),
]
