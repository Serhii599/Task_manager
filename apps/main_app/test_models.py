"""
Unit tests for models in the main_app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from .models import Project, Task, Status, Priorities
from .factories import UserFactory, ProjectFactory, TaskFactory, DataSetFactory

User = get_user_model()


class UserModelTests(TestCase):
    """Tests for User model"""
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = UserFactory.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = UserFactory.create_superuser()
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
    
    def test_user_string_representation(self):
        """Test user __str__ method returns email"""
        user = UserFactory.create_user(email="john@example.com")
        self.assertEqual(str(user), "john@example.com")


class ProjectModelTests(TestCase):
    """Tests for Project model"""
    
    def setUp(self):
        self.user = UserFactory.create_user()
    
    def test_create_project(self):
        """Test creating a project"""
        project = ProjectFactory.create_project(
            project_name="Test Project",
            creator=self.user
        )
        self.assertEqual(project.project_name, "Test Project")
        self.assertEqual(project.creator, self.user)
        self.assertIsNotNone(project.created_at)
    
    def test_project_default_values(self):
        """Test project default field values"""
        project = ProjectFactory.create_project(creator=self.user)
        self.assertEqual(project.task_count, 0)
        self.assertIn(project.status, [choice[0] for choice in Status.choices])
        self.assertIn(project.priority, [choice[0] for choice in Priorities.choices])
    
    def test_project_string_representation(self):
        """Test project __str__ method"""
        project = ProjectFactory.create_project(
            project_name="My Project",
            creator=self.user
        )
        self.assertEqual(str(project), "My Project")
    
    def test_project_with_collaborators(self):
        """Test adding collaborators to project"""
        project = ProjectFactory.create_project(creator=self.user)
        collaborators = UserFactory.create_users(count=3)
        project.collaborators.set(collaborators)
        
        self.assertEqual(project.collaborators.count(), 3)
        self.assertIn(collaborators[0], project.collaborators.all())
    
    def test_project_task_count_updates(self):
        """Test that task_count updates when tasks are added"""
        project = ProjectFactory.create_project(creator=self.user)
        tasks = TaskFactory.create_tasks(count=3, creator=self.user)
        
        project.tasks.set(tasks)
        project.refresh_from_db()
        
        self.assertEqual(project.task_count, 3)
    
    def test_project_task_count_decreases(self):
        """Test that task_count decreases when tasks are removed"""
        project = ProjectFactory.create_project(creator=self.user)
        tasks = TaskFactory.create_tasks(count=5, creator=self.user)
        project.tasks.set(tasks)
        project.refresh_from_db()
        
        # Remove 2 tasks
        project.tasks.remove(tasks[0], tasks[1])
        project.refresh_from_db()
        
        self.assertEqual(project.task_count, 3)


class TaskModelTests(TestCase):
    """Tests for Task model"""
    
    def setUp(self):
        self.creator = UserFactory.create_user(email="creator@example.com")
        self.assignee = UserFactory.create_user(email="assignee@example.com")
    
    def test_create_task(self):
        """Test creating a task"""
        task = TaskFactory.create_task(
            task_name="Test Task",
            creator=self.creator,
            assignee=self.assignee
        )
        self.assertEqual(task.task_name, "Test Task")
        self.assertEqual(task.creator, self.creator)
        self.assertEqual(task.assignee, self.assignee)
    
    def test_task_default_values(self):
        """Test task default field values"""
        task = TaskFactory.create_task(creator=self.creator)
        self.assertIn(task.status, [choice[0] for choice in Status.choices])
        self.assertIn(task.priority, [choice[0] for choice in Priorities.choices])
        self.assertIsNotNone(task.due_date)
        self.assertIsNotNone(task.created_at)
    
    def test_task_string_representation(self):
        """Test task __str__ method"""
        task = TaskFactory.create_task(
            task_name="My Task",
            creator=self.creator
        )
        self.assertEqual(str(task), "My Task")
    
    def test_task_with_collaborators(self):
        """Test adding collaborators to task"""
        task, collaborators = TaskFactory.create_task_with_collaborators(
            creator=self.creator,
            assignee=self.assignee,
            collaborator_count=4
        )
        
        self.assertEqual(task.collaborators.count(), 4)
        self.assertIn(collaborators[0], task.collaborators.all())
    
    def test_task_can_be_overdue(self):
        """Test identifying overdue tasks"""
        overdue_task = TaskFactory.create_overdue_task(creator=self.creator)
        self.assertTrue(overdue_task.due_date < timezone.now())
    
    def test_task_urgent_priority(self):
        """Test creating urgent priority task"""
        urgent_task = TaskFactory.create_urgent_task(creator=self.creator)
        self.assertEqual(urgent_task.priority, Priorities.URGENT)
    
    def test_task_completed_status(self):
        """Test completed task"""
        completed_task = TaskFactory.create_completed_task(creator=self.creator)
        self.assertEqual(completed_task.status, Status.DONE)
    
    def test_task_without_assignee(self):
        """Test task can exist without assignee"""
        task = TaskFactory.create_task(
            task_name="Unassigned Task",
            creator=self.creator,
            assignee=None
        )
        self.assertIsNone(task.assignee)
    
    def test_task_can_belong_to_multiple_projects(self):
        """Test task can be in multiple projects"""
        task = TaskFactory.create_task(creator=self.creator)
        projects = ProjectFactory.create_projects(count=3, creator=self.creator)
        
        for project in projects:
            project.tasks.add(task)
        
        self.assertEqual(task.projects.count(), 3)


class StatusAndPriorityTests(TestCase):
    """Tests for Status and Priority choices"""
    
    def test_status_choices(self):
        """Test all status choices are available"""
        expected_statuses = ['Backlog', 'To do', 'In progress', 'Done']
        actual_statuses = [choice[0] for choice in Status.choices]
        
        for status in expected_statuses:
            self.assertIn(status, actual_statuses)
    
    def test_priority_choices(self):
        """Test all priority choices are available"""
        expected_priorities = ['Low', 'Medium', 'High', 'Urgent']
        actual_priorities = [choice[0] for choice in Priorities.choices]
        
        for priority in expected_priorities:
            self.assertIn(priority, actual_priorities)


class DataSetFactoryTests(TestCase):
    """Tests for DataSetFactory"""
    
    def test_create_full_dataset(self):
        """Test creating a complete dataset"""
        dataset = DataSetFactory.create_full_dataset()
        
        self.assertIsNotNone(dataset['creator'])
        self.assertEqual(len(dataset['users']), 5)
        self.assertEqual(len(dataset['projects']), 3)
        self.assertGreaterEqual(len(dataset['tasks']), 10)
        self.assertIsNotNone(dataset['overdue_task'])
        self.assertIsNotNone(dataset['urgent_task'])
        self.assertIsNotNone(dataset['completed_task'])
    
    def test_create_project_with_full_data(self):
        """Test creating a project with complete data"""
        data = DataSetFactory.create_project_with_full_data()
        
        self.assertIsNotNone(data['project'])
        self.assertEqual(len(data['collaborators']), 3)
        self.assertGreaterEqual(len(data['tasks']), 7)
        self.assertIsNotNone(data['overdue_task'])
        self.assertIsNotNone(data['completed_task'])
        
        # Verify tasks are associated with project
        project = data['project']
        self.assertGreaterEqual(project.tasks.count(), 7)


class SignalTests(TestCase):
    """Tests for model signals"""
    
    def test_project_task_count_signal_on_add(self):
        """Test task_count updates via signal when tasks added"""
        user = UserFactory.create_user()
        project = ProjectFactory.create_project(creator=user)
        
        self.assertEqual(project.task_count, 0)
        
        # Add tasks
        tasks = TaskFactory.create_tasks(count=3, creator=user)
        project.tasks.add(*tasks)
        
        project.refresh_from_db()
        self.assertEqual(project.task_count, 3)
    
    def test_project_task_count_signal_on_remove(self):
        """Test task_count updates via signal when tasks removed"""
        user = UserFactory.create_user()
        project = ProjectFactory.create_project(creator=user)
        tasks = TaskFactory.create_tasks(count=5, creator=user)
        
        project.tasks.set(tasks)
        project.refresh_from_db()
        self.assertEqual(project.task_count, 5)
        
        # Remove tasks
        project.tasks.remove(tasks[0])
        project.refresh_from_db()
        self.assertEqual(project.task_count, 4)
    
    def test_project_task_count_signal_on_clear(self):
        """Test task_count updates via signal when all tasks cleared"""
        user = UserFactory.create_user()
        project = ProjectFactory.create_project(creator=user)
        tasks = TaskFactory.create_tasks(count=3, creator=user)
        
        project.tasks.set(tasks)
        project.refresh_from_db()
        self.assertEqual(project.task_count, 3)
        
        # Clear all tasks
        project.tasks.clear()
        project.refresh_from_db()
        self.assertEqual(project.task_count, 0)
