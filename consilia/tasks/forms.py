from django import forms

from .models import Tasks, Subtasks


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "content", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }
        labels = {"title": "Title", "content": "Content", "status": "Status"}


class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtasks
        fields = ["description", "is_done"]
        labels = {"description": "Subtask", "is_done": "Done"}
