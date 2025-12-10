"""
Unit tests for forms in the main_app.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from .forms import TaskCreationForm, ProjectCreationForm
from .models import Task, Project, Status, Priorities
from .factories import UserFactory, TaskFactory, ProjectFactory

User = TaskCreationForm.Meta.model._meta.get_field('assignee').related_model


class TaskCreationFormTests(TestCase):
    """Tests for TaskCreationForm"""
    
    def setUp(self):
        self.user = UserFactory.create_user()
    
    def test_form_has_correct_fields(self):
        """Test form has all required fields"""
        form = TaskCreationForm()
        expected_fields = ['task_name', 'task_description', 'status', 'priority', 'assignee', 'due_date', 'collaborators']
        
        for field in expected_fields:
            self.assertIn(field, form.fields)
    
    def test_valid_form_data(self):
        """Test form with valid data"""
        due_date = timezone.now() + timedelta(days=7)
        
        form_data = {
            'task_name': 'Test Task',
            'task_description': 'Test Description',
            'status': Status.TO_DO,
            'priority': Priorities.HIGH,
            'assignee': self.user.id,
            'due_date': due_date,
            'collaborators': [],
        }
        
        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_field(self):
        """Test form validation with missing required field"""
        form_data = {
            'task_description': 'Test Description',
            'status': Status.TO_DO,
            'priority': Priorities.HIGH,
            # Missing task_name
        }
        
        form = TaskCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('task_name', form.errors)
    
    def test_form_due_date_widget(self):
        """Test that due_date field uses DateTimeInput widget"""
        form = TaskCreationForm()
        widget = form.fields['due_date'].widget
        # Check if it's a DateTimeInput widget
        from django.forms.widgets import DateTimeInput
        self.assertIsInstance(widget, DateTimeInput)
    
    def test_form_save_creates_task(self):
        """Test that saving form creates a task"""
        due_date = timezone.now() + timedelta(days=7)
        
        form_data = {
            'task_name': 'New Task',
            'task_description': 'Description',
            'status': Status.TO_DO,
            'priority': Priorities.MEDIUM,
            'assignee': self.user.id,
            'due_date': due_date,
            'collaborators': [],
        }
        
        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        task = form.save()
        self.assertEqual(task.task_name, 'New Task')
        self.assertEqual(task.assignee, self.user)
        
        task = form.save()
        self.assertEqual(task.task_name, 'New Task')
        self.assertEqual(task.assignee, self.user)
    
    def test_form_with_collaborators(self):
        """Test form with multiple collaborators"""
        collaborators = UserFactory.create_users(count=3)
        due_date = timezone.now() + timedelta(days=7)
        
        form_data = {
            'task_name': 'Collaborative Task',
            'task_description': 'Description',
            'status': Status.TO_DO,
            'priority': Priorities.HIGH,
            'assignee': self.user.id,
            'due_date': due_date,
            'collaborators': [c.id for c in collaborators],
        }
        
        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        task = form.save()
        self.assertEqual(task.collaborators.count(), 3)


class ProjectCreationFormTests(TestCase):
    """Tests for ProjectCreationForm"""
    
    def setUp(self):
        self.user = UserFactory.create_user()
    
    def test_form_has_correct_fields(self):
        """Test form has all required fields"""
        form = ProjectCreationForm()
        expected_fields = ['project_name', 'project_description', 'priority', 'status', 'tasks', 'collaborators']
        
        for field in expected_fields:
            self.assertIn(field, form.fields)
    
    def test_valid_form_data(self):
        """Test form with valid data"""
        form_data = {
            'project_name': 'Test Project',
            'project_description': 'Test Description',
            'status': Status.BACKLOG,
            'priority': Priorities.MEDIUM,
        }
        
        form = ProjectCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_missing_required_field(self):
        """Test form validation with missing required field"""
        form_data = {
            'project_description': 'Description',
            'status': Status.BACKLOG,
            # Missing project_name
        }
        
        form = ProjectCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('project_name', form.errors)
    
    def test_form_save_creates_project(self):
        """Test that saving form creates a project"""
        form_data = {
            'project_name': 'New Project',
            'project_description': 'Description',
            'status': Status.IN_PROGRESS,
            'priority': Priorities.HIGH,
        }
        
        form = ProjectCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        project = form.save()
        self.assertEqual(project.project_name, 'New Project')
        self.assertEqual(project.status, Status.IN_PROGRESS)
    
    def test_form_with_tasks(self):
        """Test form with multiple tasks"""
        tasks = TaskFactory.create_tasks(count=3, creator=self.user)
        
        form_data = {
            'project_name': 'Project With Tasks',
            'project_description': 'Description',
            'status': Status.IN_PROGRESS,
            'priority': Priorities.HIGH,
            'tasks': [t.id for t in tasks],
        }
        
        form = ProjectCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        project = form.save()
        self.assertEqual(project.tasks.count(), 3)
    
    def test_form_with_collaborators(self):
        """Test form with multiple collaborators"""
        collaborators = UserFactory.create_users(count=4)
        
        form_data = {
            'project_name': 'Collaborative Project',
            'project_description': 'Description',
            'status': Status.BACKLOG,
            'priority': Priorities.MEDIUM,
            'collaborators': [c.id for c in collaborators],
        }
        
        form = ProjectCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        project = form.save()
        self.assertEqual(project.collaborators.count(), 4)
    
    def test_form_with_tasks_and_collaborators(self):
        """Test form with both tasks and collaborators"""
        tasks = TaskFactory.create_tasks(count=2, creator=self.user)
        collaborators = UserFactory.create_users(count=2)
        
        form_data = {
            'project_name': 'Full Project',
            'project_description': 'Description',
            'status': Status.IN_PROGRESS,
            'priority': Priorities.URGENT,
            'tasks': [t.id for t in tasks],
            'collaborators': [c.id for c in collaborators],
        }
        
        form = ProjectCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        project = form.save()
        self.assertEqual(project.tasks.count(), 2)
        self.assertEqual(project.collaborators.count(), 2)


class FormValidationTests(TestCase):
    """Tests for form validation edge cases"""
    
    def test_task_form_with_very_long_name(self):
        """Test task form with maximum length name"""
        user = UserFactory.create_user()
        due_date = timezone.now() + timedelta(days=7)
        
        # Task name max_length is 100
        long_name = 'A' * 100
        
        form_data = {
            'task_name': long_name,
            'task_description': 'Description',
            'status': Status.TO_DO,
            'priority': Priorities.LOW,
            'assignee': user.id,
            'due_date': due_date,
            'collaborators': [],
        }
        
        form = TaskCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_task_form_with_too_long_name(self):
        """Test task form with name exceeding max length"""
        user = UserFactory.create_user()
        due_date = timezone.now() + timedelta(days=7)
        
        # Task name max_length is 100
        too_long_name = 'A' * 101
        
        form_data = {
            'task_name': too_long_name,
            'task_description': 'Description',
            'status': Status.TO_DO,
            'priority': Priorities.LOW,
            'assignee': user.id,
            'due_date': due_date,
            'collaborators': [],
        }
        
        form = TaskCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('task_name', form.errors)
    
    def test_project_form_with_minimal_data(self):
        """Test project form with only required fields"""
        form_data = {
            'project_name': 'Minimal Project',
            'project_description': 'A description is required',
            'status': Status.BACKLOG,
            'priority': Priorities.LOW,
        }
        
        form = ProjectCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
