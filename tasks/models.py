from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="tags"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"],
                name="unique_tag_user",
            )
        ]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Task(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="tasks"
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-completed", "-created_at"]
