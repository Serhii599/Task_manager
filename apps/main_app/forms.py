from django.contrib.auth import get_user_model
from .models import Task, Project
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
        self.fields['collaborators'].required = False

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description', 'priority', 'status', 'tasks', 'collaborators']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tasks'].queryset = Task.objects.all()
        self.fields['collaborators'].queryset = User.objects.all()
        self.fields['tasks'].required = False
        self.fields['collaborators'].required = False
