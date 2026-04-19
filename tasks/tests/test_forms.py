import pytest
from datetime import timedelta
from django.utils import timezone
from django.utils.datastructures import MultiValueDict

from tasks.forms import CreateTaskForm, TagSelect2Widget
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


@pytest.mark.django_db
class TestTagSelect2Widget:
    def make_widget(self, user):
        return TagSelect2Widget(user=user)

    def call(self, widget, values):
        data = MultiValueDict({"tags": values})
        return set(widget.value_from_datadict(data, {}, "tags"))

    def test_existing_tag_pk_returned(self, test_user, tag):
        result = self.call(self.make_widget(test_user), [str(tag.pk)])
        assert result == {tag.pk}

    def test_new_tag_name_creates_tag(self, test_user):
        result = self.call(self.make_widget(test_user), ["brand-new"])
        created = Tag.objects.get(name="brand-new", user=test_user)
        assert result == {created.pk}

    def test_duplicate_name_creates_only_one_tag(self, test_user):
        widget = self.make_widget(test_user)
        self.call(widget, ["duplicate"])
        self.call(widget, ["duplicate"])
        assert Tag.objects.filter(name="duplicate", user=test_user).count() == 1

    def test_other_user_tag_pk_not_treated_as_existing(self, test_user, other_tag):
        result = self.call(self.make_widget(test_user), [str(other_tag.pk)])
        assert other_tag.pk not in result
