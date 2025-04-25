from django import forms
from .models import Project, Task, DailyWorkLog
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'manager', 'start_date', 'end_date', 'status', 'progress']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'progress': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 5}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assignee', 'parent_task', 'start_date', 'end_date', 'progress', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '작업 이름을 입력하세요'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '작업 설명을 입력하세요'}),
            'assignee': forms.Select(attrs={'class': 'form-control'}),
            'parent_task': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        if project_id:
            self.instance.project_id = project_id
            self.fields['parent_task'].queryset = Task.objects.filter(project_id=project_id)

class DailyWorkLogForm(forms.ModelForm):
    class Meta:
        model = DailyWorkLog
        fields = ['completed_tasks', 'completed_description', 'planned_tasks', 'planned_description']
        widgets = {
            'completed_tasks': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'completed_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '완료한 작업에 대한 설명을 적어주세요'}),
            'planned_tasks': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'planned_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '계획된 작업에 대한 설명을 적어주세요'}),
        }
