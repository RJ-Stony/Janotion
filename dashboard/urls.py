from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 대시보드
    path('', views.dashboard, name='dashboard'),
    
    # 인증 관련 URL
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # 프로젝트 관련 URL
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),  # Use class-based view
    path('project/<int:project_id>/update-status/', views.update_project_status, name='update-project-status'),
    
    # 작업 관련 URL
    path('project/<int:project_id>/task/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    
    # 작업 로그
    path('work-log/', views.daily_work_log_view, name='work-log'),
    path('work-log/<str:date>/', views.daily_work_log_view, name='work-log-date'),
    
    # 새로운 URL 패턴 추가
    path('update-status/', views.update_project_status, name='update-project-status'),
    
    # If you need a projects URL, uncomment and ensure the view exists
    # path('projects/', views.projects, name='projects'),
]
