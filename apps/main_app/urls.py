from django.urls import path

from .views import MyTasksListView, ProjectCreateView, TaskCreateView, UsersListView, UserTasksView, MainView, \
    ProjectDeleteView, ProjectsListView, TaskDeleteView, OneTaskDetailView, ProjectUpdateView, TaskUpdateView, \
    OneProjectListView, TaskMarkDoneView, LeaveTaskView, ProjectReportView

app_name = 'apps.main_app'

urlpatterns = [
    path('', MainView.as_view(), name='main_page'),

    path('tasks/', MyTasksListView.as_view(), name='my_tasks'),
    path('tasks/create', TaskCreateView.as_view(), name='task_create'),
    path('tasks/delete/<int:pk>', TaskDeleteView.as_view(), name='task_delete'),
    path("task/<int:task_id>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    
    path("task/<int:task_id>/mark-done/", TaskMarkDoneView.as_view(), name="task_mark_done"),
    
    path('task/<int:task_id>/', OneTaskDetailView.as_view(), name='one_task'),
    
    path("task/<int:task_id>/leave/", LeaveTaskView.as_view(), name="task_leave"),

    path('projects/', ProjectsListView.as_view(), name='projects_view'),
    path('project/create', ProjectCreateView.as_view(), name='project_create'),
    path("project/<int:project_id>/", OneProjectListView.as_view(), name="one_project"),
    path("project/<int:project_id>/edit/", ProjectUpdateView.as_view(), name="project_edit"),
    path("project/<int:project_id>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    
    path(
    "project/<int:project_id>/report/",
    ProjectReportView.as_view(),
    name="project_report"),

    path('users/', UsersListView.as_view(), name='users_list'),
    path('users/<int:user_id>', UserTasksView.as_view(), name='users_tasks')


]