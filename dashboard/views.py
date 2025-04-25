from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project, Task, DailyWorkLog
from .forms import ProjectForm, TaskForm, DailyWorkLogForm
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from datetime import date

class DashboardView(ListView):
    model = Project
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        context['today'] = today
        
        try:
            context['work_logs'] = DailyWorkLog.objects.filter(date=today)
            
            tasks = Task.objects.all()
            context['completed_tasks_count'] = tasks.filter(status='completed').count()
            context['in_progress_tasks_count'] = tasks.filter(status='in_progress').count()
            context['delayed_tasks_count'] = tasks.filter(status='delayed').count()
        except:
            context['work_logs'] = []
            context['completed_tasks_count'] = 0
            context['in_progress_tasks_count'] = 0
            context['delayed_tasks_count'] = 0
        
        for project in context['projects']:
            try:
                project_tasks = project.tasks.all()
                if project_tasks:
                    completed = sum(task.progress for task in project_tasks)
                    project.progress = int(completed / len(project_tasks))
                else:
                    project.progress = 0
                    
                project.is_completed = project_tasks.count() > 0 and all(task.status == 'completed' for task in project_tasks)
                project.is_delayed = any(task.status == 'delayed' for task in project_tasks)
            except:
                project.progress = 0
                project.is_completed = False
                project.is_delayed = False
            
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'dashboard/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.filter(parent_task__isnull=True)
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    success_url = reverse_lazy('dashboard')

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'dashboard/project_form.html'
    
    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.pk})

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'dashboard/task_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_id'] = self.kwargs.get('project_id')
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.kwargs.get('project_id')})

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'dashboard/task_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_id'] = self.object.project.id
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.project.id})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'dashboard/project_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

def daily_work_log_view(request, date=None):
    if date is None:
        date = timezone.now().date()
    log, created = DailyWorkLog.objects.get_or_create(
        date=date,
        user=request.user,
        defaults={
            'completed_description': '',
            'planned_description': ''
        }
    )
    if request.method == 'POST':
        form = DailyWorkLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('work-log')
    else:
        form = DailyWorkLogForm(instance=log)
    return render(request, 'dashboard/daily_work_log.html', {
        'form': form,
        'date': date,
        'log': log
    })

def dashboard(request):
    projects = Project.objects.all()
    planned_count = projects.filter(status='planned').count() + projects.filter(status__isnull=True).count()
    in_progress_count = projects.filter(status='in_progress').count()
    delayed_count = projects.filter(status='delayed').count()
    completed_count = projects.filter(status='completed').count()

    context = {
        'projects': projects,
        'planned_count': planned_count,
        'in_progress_count': in_progress_count,
        'delayed_count': delayed_count,
        'completed_count': completed_count,
    }

    return render(request, 'dashboard/dashboard.html', context)

@require_POST
def update_project_status(request):
    try:
        data = json.loads(request.body)
        project_id = data.get('project_id')
        new_status = data.get('new_status')
        project = get_object_or_404(Project, id=project_id)
        valid_statuses = ['planned', 'in_progress', 'delayed', 'completed']
        if new_status not in valid_statuses:
            return JsonResponse({'error': '유효하지 않은 상태입니다.'}, status=400)
        project.status = new_status
        if new_status == 'completed' and project.progress != 100:
            project.progress = 100
        project.save()
        return JsonResponse({'success': True})
    except Project.DoesNotExist:
        return JsonResponse({'error': '프로젝트를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
