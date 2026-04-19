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
