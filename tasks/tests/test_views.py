import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUnauthenticatedAccess:
    def test_task_list_redirects(self, client):
        assert client.get(reverse("tasks:index")).status_code == 302

    def test_task_create_redirects(self, client):
        assert client.get(reverse("tasks:task-create")).status_code == 302

    def test_task_update_redirects(self, client, task):
        assert (
            client.get(
                reverse("tasks:task-update", kwargs={"pk": task.pk})
            ).status_code
            == 302
        )

    def test_task_delete_redirects(self, client, task):
        assert (
            client.get(
                reverse("tasks:task-delete", kwargs={"pk": task.pk})
            ).status_code
            == 302
        )

    def test_tag_list_redirects(self, client):
        assert client.get(reverse("tasks:tag-list")).status_code == 302

    def test_tag_create_redirects(self, client):
        assert client.get(reverse("tasks:tag-create")).status_code == 302

    def test_tag_update_redirects(self, client, tag):
        assert (
            client.get(
                reverse("tasks:tag-update", kwargs={"pk": tag.pk})
            ).status_code
            == 302
        )

    def test_tag_delete_redirects(self, client, tag):
        assert (
            client.get(
                reverse("tasks:tag-delete", kwargs={"pk": tag.pk})
            ).status_code
            == 302
        )


@pytest.mark.django_db
class TestCrossUserAccess:
    def test_cannot_update_other_user_task(
        self, client, test_user, other_task
    ):
        client.force_login(test_user)
        assert (
            client.get(
                reverse("tasks:task-update", kwargs={"pk": other_task.pk})
            ).status_code
            == 404
        )

    def test_cannot_delete_other_user_task(
        self, client, test_user, other_task
    ):
        client.force_login(test_user)
        assert (
            client.get(
                reverse("tasks:task-delete", kwargs={"pk": other_task.pk})
            ).status_code
            == 404
        )

    def test_cannot_update_other_user_tag(self, client, test_user, other_tag):
        client.force_login(test_user)
        assert (
            client.get(
                reverse("tasks:tag-update", kwargs={"pk": other_tag.pk})
            ).status_code
            == 404
        )

    def test_cannot_delete_other_user_tag(self, client, test_user, other_tag):
        client.force_login(test_user)
        assert (
            client.get(
                reverse("tasks:tag-delete", kwargs={"pk": other_tag.pk})
            ).status_code
            == 404
        )

    def test_cannot_complete_other_user_task(
        self, client, test_user, other_task
    ):
        client.force_login(test_user)
        assert (
            client.post(
                reverse("tasks:task-complete", kwargs={"pk": other_task.pk})
            ).status_code
            == 404
        )

    def test_cannot_undo_other_user_task(
        self, client, test_user, other_task
    ):
        client.force_login(test_user)
        assert (
            client.post(
                reverse("tasks:task-undo", kwargs={"pk": other_task.pk})
            ).status_code
            == 404
        )


@pytest.mark.django_db
class TestCompleteUndoTask:
    def test_complete_task(self, client, test_user, task):
        client.force_login(test_user)
        client.post(reverse("tasks:task-complete", kwargs={"pk": task.pk}))
        task.refresh_from_db()
        assert task.completed is True

    def test_undo_task(self, client, test_user, task):
        task.completed = True
        task.save()
        client.force_login(test_user)
        client.post(reverse("tasks:task-undo", kwargs={"pk": task.pk}))
        task.refresh_from_db()
        assert task.completed is False


@pytest.mark.django_db
class TestSearchTasks:
    def test_returns_only_own_tasks(self, client, test_user, other_user):
        from tasks.models import Task
        Task.objects.create(content="my task", user=test_user)
        Task.objects.create(content="my task", user=other_user)
        client.force_login(test_user)
        response = client.get(reverse("tasks:task-search") + "?q=my task")
        assert len(response.context["tasks"]) == 1

    def test_filters_by_content(self, client, test_user):
        from tasks.models import Task
        Task.objects.create(content="buy milk", user=test_user)
        Task.objects.create(content="call doctor", user=test_user)
        client.force_login(test_user)
        response = client.get(reverse("tasks:task-search") + "?q=milk")
        assert len(response.context["tasks"]) == 1
        assert response.context["tasks"][0].content == "buy milk"
