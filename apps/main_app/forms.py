from django.contrib.auth import get_user_model
from .models import Task, Project, Comment
from django import forms

User = get_user_model()


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'task_description', 'status', 'priority', 'assignee','due_date', 'collaborators']
        widgets = {
            'due_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                }
            ),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # список усіх юзерів у випадаючому списку
            self.fields['assignee'].queryset = User.objects.all()
            self.fields['collaborators'].queryset = User.objects.all()

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'priority', 'status', 'tasks', 'collaborators']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tasks'].queryset = Task.objects.all()
        self.fields['collaborators'].queryset = User.objects.all()

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write a comment...',
                'class': 'comment-textarea',
            }),
        }
