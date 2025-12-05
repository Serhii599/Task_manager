from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_object_or_404

from .forms import TaskCreationForm, ProjectCreationForm
from .models import *

User = get_user_model()


class MainView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main_app:my_tasks')
        else:
            return redirect('authentication:login')


class MyTasksListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'main_app/my_task_list.html'

    def get_queryset(self):
        qs = Task.objects.filter(assignee=self.request.user)

        # === СОРТУВАННЯ =====================================================
        ordering = self.request.GET.get("sort")

        sortable_fields = ["task_name", "due_date", "priority", "status"]

        if ordering in sortable_fields:
            qs = qs.order_by(ordering)
        elif ordering and ordering.startswith("-") and ordering[1:] in sortable_fields:
            qs = qs.order_by(ordering)

        # === ФІЛЬТРАЦІЯ ======================================================
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")

        if status:
            qs = qs.filter(status=status)

        if priority:
            qs = qs.filter(priority=priority)

        return qs

class OneTaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'main_app/one_task.html'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task = self.object  # поточна задача

        # знаходимо інші задачі того самого виконавця
        context["other_tasks"] = (
            Task.objects
            .filter(assignee=task.assignee)
            .exclude(id=task.id)
            .order_by("due_date")
        )

        return context

class ProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'main_app/projects_list.html'


class OneProjectListView(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'main_app/one_project.html'
    pk_url_kwarg = 'project_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = self.object
        tasks = Task.objects.filter(projects=project)

        # --- FILTERING ---
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        sort = self.request.GET.get("sort")

        if status:
            tasks = tasks.filter(status=status)
            

        if priority:
            tasks = tasks.filter(priority=priority)

        # --- SORTING ---
        valid_sorts = [
            "task_name",
            "due_date",
            "status",
            "priority",
            "assignee__first_name",
        ]

        # --- SORTING ---
        if sort:

            # PRIORITY sorting (custom)
            if sort == "priority":
                order = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}
                tasks = sorted(tasks, key=lambda t: order.get(t.priority, 999))

            elif sort == "-priority":
                order = {"Urgent": 4, "High": 3, "Medium": 2, "Low": 1}
                tasks = sorted(tasks, key=lambda t: order.get(t.priority, 0))

            # STATUS sorting (custom)
            elif sort == "status":
                order = {
                    "Done": 1,
                    "In progress": 2,
                    "To do": 3,
                    "Backlog": 4,
                }
                tasks = sorted(tasks, key=lambda t: order.get(t.status, 999))

            elif sort == "-status":
                order = {
                    "Done": 4,
                    "In progress": 3,
                    "To do": 2,
                    "Backlog": 1,
                }
                tasks = sorted(tasks, key=lambda t: order.get(t.status, 0))

            # NORMAL DJANGO SORT
            else:
                base = sort.lstrip("-")
                valid_sorts = ["task_name", "due_date", "assignee__first_name"]
                if base in valid_sorts:
                    tasks = tasks.order_by(sort)

        context["tasks"] = tasks
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = "main_app/project_create.html"
    success_url = reverse_lazy("main_app:project_create")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskCreationForm
    template_name = "main_app/task_create.html"
    success_url = reverse_lazy("main_app:task_create")

    def form_valid(self, form):
        # приклад, якщо треба підв’язати користувача
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'main_app/project_edit.html'
    pk_url_kwarg = 'project_id'

    def get_success_url(self):
        return reverse_lazy("main_app:one_project", kwargs={"project_id": self.object.id})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskCreationForm
    template_name = 'main_app/task_edit.html'
    pk_url_kwarg = 'task_id'

    def get_success_url(self):
        return reverse_lazy("main_app:one_task", kwargs={"task_id": self.object.id})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    pk_url_kwarg = 'project_id'
    template_name = "main_app/project_confirm_delete.html"
    success_url = reverse_lazy("main_app:projects_view")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('main_app:my_tasks')

class UsersListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'main_app/users_list.html'

class UserTasksView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'main_app/user_tasks.html'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(assignee_id=user_id).select_related('assignee')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']

        # спробуємо отримати користувача без try/except через get_object_or_404:
        context['user'] = get_object_or_404(User, id=user_id)

        return context
    
class TaskMarkDoneView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        # Дозволити змінювати тільки виконавцю або автору
        if task.assignee != request.user and task.creator != request.user:
            return HttpResponse("Forbidden", status=403)

        task.status = "Done"
        task.save()

        return redirect('main_app:one_task', task_id=task.id)
    
class LeaveTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        user = request.user

        # Якщо юзер є асайні — знімаємо його
        if task.assignee == user:
            task.assignee = None

        # Якщо юзер є серед колабораторів — видаляємо
        if user in task.collaborators.all():
            task.collaborators.remove(user)

        task.save()
        return redirect("main_app:my_tasks")
    
class ProjectReportView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "main_app/project_report.html"
    context_object_name = "project"
    pk_url_kwarg = "project_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = self.object
        tasks = Task.objects.filter(projects=project)

        # ===========================
        # 1. TOP 3 BY DEADLINE
        # ===========================
        top_by_deadline = tasks.exclude(due_date=None).order_by("due_date")[:3]

        # ===========================
        # 2. TOP 3 BY PRIORITY (custom ordering)
        # ===========================
        priority_order = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}

        top_by_priority = sorted(
            tasks,
            key=lambda t: priority_order.get(t.priority, 999)
        )[:3]

        # ===========================
        # 3. OVERDUE TASKS
        # ===========================
        from django.utils import timezone
        now = timezone.now()

        overdue_tasks = tasks.filter(
            due_date__lt=now
        ).exclude(
            status="Done"
        ).order_by("due_date")

        # ===========================
        # 4. TOTAL DONE TASKS
        # ===========================
        total_done = tasks.filter(status="Done").count()

        # ===========================
        # Add to context
        # ===========================
        context["top_by_deadline"] = top_by_deadline
        context["top_by_priority"] = top_by_priority
        context["overdue_tasks"] = overdue_tasks
        context["total_done"] = total_done

        return context
