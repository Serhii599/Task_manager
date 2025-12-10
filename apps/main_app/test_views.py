"""
Unit tests for views in the main_app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Project, Task, Status, Priorities
from .factories import UserFactory, ProjectFactory, TaskFactory, DataSetFactory

User = get_user_model()


class MainViewTests(TestCase):
    """Tests for MainView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
    
    def test_redirect_authenticated_user_to_tasks(self):
        """Test authenticated user is redirected to my_tasks"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('main_app:main_page'))
        self.assertRedirects(response, reverse('main_app:my_tasks'))
    
    def test_redirect_anonymous_user_to_login(self):
        """Test anonymous user is redirected to login"""
        response = self.client.get(reverse('main_app:main_page'))
        self.assertRedirects(response, reverse('authentication:login'))


class MyTasksListViewTests(TestCase):
    """Tests for MyTasksListView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.other_user = UserFactory.create_user(email="other@example.com")
        self.client.force_login(self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:my_tasks'))
        self.assertEqual(response.status_code, 302)
    
    def test_shows_only_user_tasks(self):
        """Test view shows only tasks assigned to current user"""
        my_tasks = TaskFactory.create_tasks(count=3, assignee=self.user)
        other_tasks = TaskFactory.create_tasks(count=2, assignee=self.other_user)
        
        response = self.client.get(reverse('main_app:my_tasks'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 3)
        
        for task in my_tasks:
            self.assertIn(task, response.context['tasks'])
        
        for task in other_tasks:
            self.assertNotIn(task, response.context['tasks'])
    
    def test_filter_by_status(self):
        """Test filtering tasks by status"""
        TaskFactory.create_task(assignee=self.user, status=Status.TO_DO)
        TaskFactory.create_task(assignee=self.user, status=Status.TO_DO)
        TaskFactory.create_task(assignee=self.user, status=Status.DONE)
        
        response = self.client.get(reverse('main_app:my_tasks'), {'status': Status.TO_DO})
        
        self.assertEqual(len(response.context['tasks']), 2)
        for task in response.context['tasks']:
            self.assertEqual(task.status, Status.TO_DO)
    
    def test_filter_by_priority(self):
        """Test filtering tasks by priority"""
        TaskFactory.create_task(assignee=self.user, priority=Priorities.URGENT)
        TaskFactory.create_task(assignee=self.user, priority=Priorities.LOW)
        TaskFactory.create_task(assignee=self.user, priority=Priorities.URGENT)
        
        response = self.client.get(reverse('main_app:my_tasks'), {'priority': Priorities.URGENT})
        
        self.assertEqual(len(response.context['tasks']), 2)
        for task in response.context['tasks']:
            self.assertEqual(task.priority, Priorities.URGENT)
    
    def test_sort_by_task_name(self):
        """Test sorting tasks by name"""
        TaskFactory.create_task(task_name="Zebra Task", assignee=self.user)
        TaskFactory.create_task(task_name="Alpha Task", assignee=self.user)
        TaskFactory.create_task(task_name="Beta Task", assignee=self.user)
        
        response = self.client.get(reverse('main_app:my_tasks'), {'sort': 'task_name'})
        
        tasks = list(response.context['tasks'])
        self.assertEqual(tasks[0].task_name, "Alpha Task")
        self.assertEqual(tasks[1].task_name, "Beta Task")
        self.assertEqual(tasks[2].task_name, "Zebra Task")


class OneTaskDetailViewTests(TestCase):
    """Tests for OneTaskDetailView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
        self.task = TaskFactory.create_task(assignee=self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:one_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_view_task_detail(self):
        """Test viewing task details"""
        response = self.client.get(reverse('main_app:one_task', kwargs={'task_id': self.task.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'], self.task)
    
    def test_shows_other_tasks_of_same_assignee(self):
        """Test view shows other tasks of the same assignee"""
        other_task1 = TaskFactory.create_task(assignee=self.user, task_name="Other Task 1")
        other_task2 = TaskFactory.create_task(assignee=self.user, task_name="Other Task 2")
        different_assignee_task = TaskFactory.create_task(
            assignee=UserFactory.create_user(email="another@example.com")
        )
        
        response = self.client.get(reverse('main_app:one_task', kwargs={'task_id': self.task.id}))
        other_tasks = response.context['other_tasks']
        
        self.assertIn(other_task1, other_tasks)
        self.assertIn(other_task2, other_tasks)
        self.assertNotIn(self.task, other_tasks)  # Current task should not be in other_tasks
        self.assertNotIn(different_assignee_task, other_tasks)


class ProjectsListViewTests(TestCase):
    """Tests for ProjectsListView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:projects_view'))
        self.assertEqual(response.status_code, 302)
    
    def test_view_projects_list(self):
        """Test viewing list of projects"""
        projects = ProjectFactory.create_projects(count=3, creator=self.user)
        
        response = self.client.get(reverse('main_app:projects_view'))
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.context['projects']), 3)


class OneProjectListViewTests(TestCase):
    """Tests for OneProjectListView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
        self.project = ProjectFactory.create_project(creator=self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:one_project', kwargs={'project_id': self.project.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_view_project_detail(self):
        """Test viewing project details"""
        response = self.client.get(reverse('main_app:one_project', kwargs={'project_id': self.project.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], self.project)


class TaskCreateViewTests(TestCase):
    """Tests for TaskCreateView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:task_create'))
        self.assertEqual(response.status_code, 302)
    
    def test_get_task_create_form(self):
        """Test GET request shows task creation form"""
        response = self.client.get(reverse('main_app:task_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_create_task(self):
        """Test POST request creates a new task"""
        from django.utils import timezone
        
        data = {
            'task_name': 'New Test Task',
            'task_description': 'Description',
            'status': Status.TO_DO,
            'priority': Priorities.HIGH,
            'due_date': (timezone.now() + timezone.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
            'assignee': self.user.id,
            'collaborators': [],
        }
        
        response = self.client.post(reverse('main_app:task_create'), data)
        
        self.assertEqual(Task.objects.filter(task_name='New Test Task').count(), 1)
        new_task = Task.objects.get(task_name='New Test Task')
        self.assertEqual(new_task.creator, self.user)


class ProjectCreateViewTests(TestCase):
    """Tests for ProjectCreateView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:project_create'))
        self.assertEqual(response.status_code, 302)
    
    def test_get_project_create_form(self):
        """Test GET request shows project creation form"""
        response = self.client.get(reverse('main_app:project_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_create_project(self):
        """Test POST request creates a new project"""
        data = {
            'project_name': 'New Test Project',
            'project_description': 'Project Description',
            'status': Status.BACKLOG,
            'priority': Priorities.MEDIUM,
            'tasks': [],
            'collaborators': [],
        }
        
        response = self.client.post(reverse('main_app:project_create'), data)
        
        self.assertEqual(Project.objects.filter(project_name='New Test Project').count(), 1)
        new_project = Project.objects.get(project_name='New Test Project')
        self.assertEqual(new_project.creator, self.user)


class TaskUpdateViewTests(TestCase):
    """Tests for TaskUpdateView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
        self.task = TaskFactory.create_task(creator=self.user, assignee=self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:task_edit', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_get_task_edit_form(self):
        """Test GET request shows task edit form"""
        response = self.client.get(reverse('main_app:task_edit', kwargs={'task_id': self.task.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
    
    def test_update_task(self):
        """Test POST request updates task"""
        data = {
            'task_name': 'Updated Task Name',
            'task_description': self.task.task_description,
            'status': Status.IN_PROGRESS,
            'priority': self.task.priority,
            'due_date': self.task.due_date.strftime('%Y-%m-%d %H:%M:%S'),
            'assignee': self.user.id,
            'collaborators': [],
        }
        
        response = self.client.post(
            reverse('main_app:task_edit', kwargs={'task_id': self.task.id}),
            data
        )
        
        self.task.refresh_from_db()
        self.assertEqual(self.task.task_name, 'Updated Task Name')
        self.assertEqual(self.task.status, Status.IN_PROGRESS)


class TaskDeleteViewTests(TestCase):
    """Tests for TaskDeleteView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
        self.task = TaskFactory.create_task(creator=self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:task_delete', kwargs={'pk': self.task.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_delete_task(self):
        """Test deleting a task"""
        task_id = self.task.id
        response = self.client.post(reverse('main_app:task_delete', kwargs={'pk': task_id}))
        
        self.assertFalse(Task.objects.filter(id=task_id).exists())


class ProjectDeleteViewTests(TestCase):
    """Tests for ProjectDeleteView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
        self.project = ProjectFactory.create_project(creator=self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:project_delete', kwargs={'project_id': self.project.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_delete_project(self):
        """Test deleting a project"""
        project_id = self.project.id
        response = self.client.post(reverse('main_app:project_delete', kwargs={'project_id': project_id}))
        
        self.assertFalse(Project.objects.filter(id=project_id).exists())


class UsersListViewTests(TestCase):
    """Tests for UsersListView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:users_list'))
        self.assertEqual(response.status_code, 302)
    
    def test_view_users_list(self):
        """Test viewing list of users"""
        UserFactory.create_users(count=5)
        
        response = self.client.get(reverse('main_app:users_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.context['users']), 5)


class UserTasksViewTests(TestCase):
    """Tests for UserTasksView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.target_user = UserFactory.create_user(email="target@example.com")
        self.client.force_login(self.user)
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:users_tasks', kwargs={'user_id': self.target_user.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_view_user_tasks(self):
        """Test viewing tasks of a specific user"""
        TaskFactory.create_tasks(count=3, assignee=self.target_user)
        TaskFactory.create_tasks(count=2, assignee=self.user)
        
        response = self.client.get(reverse('main_app:users_tasks', kwargs={'user_id': self.target_user.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 3)


class ProjectReportViewTests(TestCase):
    """Tests for ProjectReportView"""
    
    def setUp(self):
        self.client = Client()
        self.user = UserFactory.create_user()
        self.client.force_login(self.user)
        
        # Create project with tasks
        data = DataSetFactory.create_project_with_full_data(creator=self.user)
        self.project = data['project']
    
    def test_login_required(self):
        """Test view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('main_app:project_report', kwargs={'project_id': self.project.id}))
        self.assertEqual(response.status_code, 302)
    
    def test_view_project_report(self):
        """Test viewing project report"""
        response = self.client.get(reverse('main_app:project_report', kwargs={'project_id': self.project.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('project', response.context)
        self.assertIn('total_done', response.context)
        self.assertIn('overdue_tasks', response.context)
