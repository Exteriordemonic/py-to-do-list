import pytest
from tasks.models import Tag


def test_tag_unique_constraint(test_user):
    Tag.objects.create(name="work", user=test_user)
    with pytest.raises(Exception):
        Tag.objects.create(name="work", user=test_user)
