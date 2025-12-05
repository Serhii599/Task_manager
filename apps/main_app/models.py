from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils import timezone


User = get_user_model()

class Status(models.TextChoices):
    BACKLOG = 'Backlog'
    TO_DO = 'To do'
    IN_PROGRESS = 'In progress'
    DONE = 'Done'


class Priorities(models.TextChoices):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    URGENT = 'Urgent'

class Project(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.BACKLOG)
    priority = models.CharField(max_length=100, choices=Priorities.choices, default=Priorities.LOW)
    task_count = models.PositiveIntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_project', null=True, blank=True)
    tasks = models.ManyToManyField('Task', related_name='projects')
    collaborators = models.ManyToManyField(User, related_name="collaborating_projects")

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project_name

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    task_description = models.TextField(null=True)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.BACKLOG)
    priority = models.CharField(max_length=100, choices=Priorities.choices, default=Priorities.LOW)
    due_date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_task', null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    collaborators = models.ManyToManyField(User, related_name="collaborating_tasks")

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task_name

@receiver(m2m_changed, sender=Project.tasks.through)
def update_tasks_count(sender, instance, **kwargs):
    instance.task_count = instance.tasks.count()
    instance.save(update_fields=['task_count'])
