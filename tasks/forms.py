from django import forms
from tasks.models import Task, Tag


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["content", "deadline", "tags"]
        widgets = {
            "content": forms.TextInput(attrs={"class": "form-control"}),
            "deadline": forms.DateTimeInput(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(
                attrs={"class": "form-control select2", "data-tags": "true"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.all()
