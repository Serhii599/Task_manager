"""
Factory file for creating test data.
Provides functions for mass filling of tables with test information.
"""
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from .models import Project, Task, Status, Priorities

User = get_user_model()


class UserFactory:
    """Factory for creating User instances"""
    
    @staticmethod
    def create_user(email=None, password="testpass123", first_name=None, last_name=None, **kwargs):
        """Create a single user"""
        if not email:
            email = f"user_{random.randint(1000, 9999)}@example.com"
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name or f"FirstName{random.randint(1, 100)}",
            last_name=last_name or f"LastName{random.randint(1, 100)}",
            **kwargs
        )
        return user
    
    @staticmethod
    def create_users(count=5):
        """Create multiple users"""
        users = []
        for i in range(count):
            user = UserFactory.create_user(
                email=f"testuser{i}@example.com",
                first_name=f"User{i}",
                last_name=f"Test{i}"
            )
            users.append(user)
        return users
    
    @staticmethod
    def create_superuser(email="admin@example.com", password="admin123"):
        """Create a superuser"""
        return User.objects.create_user(
            email=email,
            password=password,
            is_superuser=True,
            is_staff=True
        )


class ProjectFactory:
    """Factory for creating Project instances"""
    
    @staticmethod
    def create_project(
        project_name=None,
        creator=None,
        status=None,
        priority=None,
        **kwargs
    ):
        """Create a single project"""
        if not project_name:
            project_name = f"Test Project {random.randint(1000, 9999)}"
        
        project = Project.objects.create(
            project_name=project_name,
            project_description=kwargs.get('project_description', f"Description for {project_name}"),
            status=status or random.choice(list(Status.choices))[0],
            priority=priority or random.choice(list(Priorities.choices))[0],
            creator=creator,
        )
        return project
    
    @staticmethod
    def create_projects(count=5, creator=None):
        """Create multiple projects"""
        projects = []
        for i in range(count):
            project = ProjectFactory.create_project(
                project_name=f"Project {i}",
                creator=creator,
                status=random.choice(list(Status.choices))[0],
                priority=random.choice(list(Priorities.choices))[0]
            )
            projects.append(project)
        return projects
    
    @staticmethod
    def create_project_with_collaborators(creator=None, collaborator_count=3):
        """Create a project with collaborators"""
        project = ProjectFactory.create_project(creator=creator)
        collaborators = UserFactory.create_users(collaborator_count)
        project.collaborators.set(collaborators)
        return project, collaborators


class TaskFactory:
    """Factory for creating Task instances"""
    
    @staticmethod
    def create_task(
        task_name=None,
        creator=None,
        assignee=None,
        status=None,
        priority=None,
        due_date=None,
        **kwargs
    ):
        """Create a single task"""
        if not task_name:
            task_name = f"Test Task {random.randint(1000, 9999)}"
        
        if not due_date:
            # Random due date between -7 and +14 days from now
            days_offset = random.randint(-7, 14)
            due_date = timezone.now() + timedelta(days=days_offset)
        
        task = Task.objects.create(
            task_name=task_name,
            task_description=kwargs.get('task_description', f"Description for {task_name}"),
            status=status or random.choice(list(Status.choices))[0],
            priority=priority or random.choice(list(Priorities.choices))[0],
            due_date=due_date,
            creator=creator,
            assignee=assignee,
        )
        return task
    
    @staticmethod
    def create_tasks(count=5, creator=None, assignee=None):
        """Create multiple tasks"""
        tasks = []
        for i in range(count):
            task = TaskFactory.create_task(
                task_name=f"Task {i}",
                creator=creator,
                assignee=assignee,
                status=random.choice(list(Status.choices))[0],
                priority=random.choice(list(Priorities.choices))[0]
            )
            tasks.append(task)
        return tasks
    
    @staticmethod
    def create_overdue_task(creator=None, assignee=None):
        """Create an overdue task"""
        return TaskFactory.create_task(
            task_name="Overdue Task",
            creator=creator,
            assignee=assignee,
            status=Status.TO_DO,
            due_date=timezone.now() - timedelta(days=5)
        )
    
    @staticmethod
    def create_urgent_task(creator=None, assignee=None):
        """Create an urgent priority task"""
        return TaskFactory.create_task(
            task_name="Urgent Task",
            creator=creator,
            assignee=assignee,
            priority=Priorities.URGENT,
            due_date=timezone.now() + timedelta(days=1)
        )
    
    @staticmethod
    def create_completed_task(creator=None, assignee=None):
        """Create a completed task"""
        return TaskFactory.create_task(
            task_name="Completed Task",
            creator=creator,
            assignee=assignee,
            status=Status.DONE,
            due_date=timezone.now() - timedelta(days=2)
        )
    
    @staticmethod
    def create_task_with_collaborators(creator=None, assignee=None, collaborator_count=3):
        """Create a task with collaborators"""
        task = TaskFactory.create_task(creator=creator, assignee=assignee)
        collaborators = UserFactory.create_users(collaborator_count)
        task.collaborators.set(collaborators)
        return task, collaborators


class DataSetFactory:
    """Factory for creating complete data sets"""
    
    @staticmethod
    def create_full_dataset():
        """
        Create a complete dataset with users, projects, and tasks.
        Returns a dictionary with all created objects.
        """
        # Create users
        creator = UserFactory.create_user(email="creator@example.com", first_name="John", last_name="Creator")
        users = UserFactory.create_users(count=5)
        
        # Create projects
        projects = []
        for i in range(3):
            project = ProjectFactory.create_project(
                project_name=f"Project {i+1}",
                creator=creator,
                status=random.choice(list(Status.choices))[0],
                priority=random.choice(list(Priorities.choices))[0]
            )
            # Add some collaborators
            project.collaborators.set(random.sample(users, k=min(3, len(users))))
            projects.append(project)
        
        # Create tasks
        tasks = []
        for i in range(10):
            task = TaskFactory.create_task(
                task_name=f"Task {i+1}",
                creator=creator,
                assignee=random.choice(users) if i % 2 == 0 else None,
                status=random.choice(list(Status.choices))[0],
                priority=random.choice(list(Priorities.choices))[0]
            )
            tasks.append(task)
            
            # Assign some tasks to projects
            if i < 6:
                project_index = i % len(projects)
                projects[project_index].tasks.add(task)
        
        # Create some specific scenario tasks
        overdue_task = TaskFactory.create_overdue_task(creator=creator, assignee=users[0])
        urgent_task = TaskFactory.create_urgent_task(creator=creator, assignee=users[1])
        completed_task = TaskFactory.create_completed_task(creator=creator, assignee=users[2])
        
        tasks.extend([overdue_task, urgent_task, completed_task])
        
        return {
            'creator': creator,
            'users': users,
            'projects': projects,
            'tasks': tasks,
            'overdue_task': overdue_task,
            'urgent_task': urgent_task,
            'completed_task': completed_task,
        }
    
    @staticmethod
    def create_project_with_full_data(creator=None):
        """
        Create a project with tasks and collaborators.
        Useful for testing project-specific features.
        """
        if not creator:
            creator = UserFactory.create_user(email="project_creator@example.com")
        
        project = ProjectFactory.create_project(
            project_name="Full Featured Project",
            creator=creator,
            status=Status.IN_PROGRESS,
            priority=Priorities.HIGH
        )
        
        # Add collaborators
        collaborators = UserFactory.create_users(count=3)
        project.collaborators.set(collaborators)
        
        # Add various tasks
        tasks = []
        
        # Regular tasks
        for i in range(5):
            task = TaskFactory.create_task(
                task_name=f"Project Task {i+1}",
                creator=creator,
                assignee=random.choice(collaborators),
                status=random.choice(list(Status.choices))[0],
                priority=random.choice(list(Priorities.choices))[0]
            )
            project.tasks.add(task)
            tasks.append(task)
        
        # Add one overdue task
        overdue = TaskFactory.create_overdue_task(creator=creator, assignee=collaborators[0])
        project.tasks.add(overdue)
        tasks.append(overdue)
        
        # Add one completed task
        completed = TaskFactory.create_completed_task(creator=creator, assignee=collaborators[1])
        project.tasks.add(completed)
        tasks.append(completed)
        
        return {
            'project': project,
            'creator': creator,
            'collaborators': collaborators,
            'tasks': tasks,
            'overdue_task': overdue,
            'completed_task': completed,
        }
