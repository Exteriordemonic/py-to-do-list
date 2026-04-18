from django import forms
from django.utils import timezone
from django_select2.forms import ModelSelect2TagWidget

from tasks.models import Task, Tag


class TagSelect2Widget(ModelSelect2TagWidget):
    model = Tag
    queryset = Tag.objects.none()
    search_fields = ["name__icontains"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.queryset = Tag.objects.filter(user=self.user)

    def label_from_instance(self, obj):
        return obj.name

    def value_from_datadict(self, data, files, name):
        values = set(super().value_from_datadict(data, files, name))
        existing_pks = set()
        created_pks = set()

        for value in values:
            if value.isdigit() and self.queryset.get(pk=int(value)):
                existing_pks.add(int(value))
            else:
                tag, _ = Tag.objects.get_or_create(
                    name=value.strip(), user=self.user
                )
                created_pks.add(tag.pk)

        return list(existing_pks | created_pks)


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["content", "deadline", "tags"]
        widgets = {
            "content": forms.TextInput(attrs={"class": "form-control"}),
            "deadline": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["tags"].queryset = Tag.objects.filter(user=self.user)
        self.fields["tags"].widget = TagSelect2Widget(
            user=self.user,
            attrs={
                "class": "form-control select2",
                "data-placeholder": "Select or create tags",
                "data-minimum-input-length": 0,
            },
        )
        self.fields["tags"].widget.choices = self.fields["tags"].choices

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Deadline cannot be in the past.")
        return deadline

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user

        if commit:
            instance.save()
            self.save_m2m()

        return instance
