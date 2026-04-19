import pytest
from django.contrib.auth import get_user_model
from tasks.models import Tag, Task

User = get_user_model()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="otheruser", password="otherpass")


@pytest.fixture
def task(test_user):
    return Task.objects.create(content="My task", user=test_user)


@pytest.fixture
def other_task(other_user):
    return Task.objects.create(content="Other task", user=other_user)


@pytest.fixture
def tag(test_user):
    return Tag.objects.create(name="my-tag", user=test_user)


@pytest.fixture
def other_tag(other_user):
    return Tag.objects.create(name="other-tag", user=other_user)
