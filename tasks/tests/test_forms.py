from datetime import timedelta
from django.utils import timezone

from tasks.forms import CreateTaskForm
from tasks.models import Tag


class TestCreateTaskForm:
    def test_valid_form(self, test_user):
        form = CreateTaskForm(
            data={
                "content": "Test task",
                "deadline": timezone.now() + timedelta(days=1),
                "tags": [tag.pk for tag in Tag.objects.filter(user=test_user)],
            },
            user=test_user,
        )
        assert form.is_valid()

    def test_invalid_form(self, test_user):
        form = CreateTaskForm(
            data={
                "content": "",
                "deadline": timezone.now(),
                "tags": [tag.pk for tag in Tag.objects.filter(user=test_user)],
            },
            user=test_user,
        )
        assert not form.is_valid()
        assert "content" in form.errors

    def test_deadline_in_past(self, test_user):
        form = CreateTaskForm(
            data={
                "content": "Test task",
                "deadline": timezone.now() - timedelta(days=1),
                "tags": [tag.pk for tag in Tag.objects.filter(user=test_user)],
            },
            user=test_user,
        )
        assert not form.is_valid()
        assert "deadline" in form.errors
