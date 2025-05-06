from django import forms

from .models import Tasks


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'title': 'Title', 'content': 'Content', 'status': 'Status'}