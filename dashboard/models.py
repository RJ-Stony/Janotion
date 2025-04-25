from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('planned', '계획됨'),
        ('in_progress', '진행중'),
        ('delayed', '지연'),
        ('completed', '완료'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='프로젝트명')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_projects', verbose_name='담당자')
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(verbose_name='종료일')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name='상태'
    )
    progress = models.IntegerField(default=0, verbose_name='진행률')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '프로젝트'
        verbose_name_plural = '프로젝트'

class Task(models.Model):
    STATUS_CHOICES = (
        ('planned', '계획됨'),
        ('in_progress', '진행중'),
        ('completed', '완료'),
        ('delayed', '지연'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='프로젝트')
    name = models.CharField(max_length=200, verbose_name='작업명')
    description = models.TextField(blank=True, null=True, verbose_name='설명')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', verbose_name='담당자')
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subtasks', verbose_name='상위 작업')
    task_order = models.PositiveIntegerField(default=0, verbose_name='작업 순서')
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(verbose_name='종료일')
    progress = models.IntegerField(default=0, verbose_name='진행률(%)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name='상태')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '작업'
        verbose_name_plural = '작업'
        ordering = ['task_order']

class DailyWorkLog(models.Model):
    date = models.DateField(verbose_name='날짜')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_logs', verbose_name='사용자')
    completed_tasks = models.ManyToManyField(Task, related_name='completed_in_logs', verbose_name='완료된 작업')
    completed_description = models.TextField(verbose_name='완료된 작업 설명')
    planned_tasks = models.ManyToManyField(Task, related_name='planned_in_logs', verbose_name='예정된 작업')
    planned_description = models.TextField(verbose_name='예정된 작업 설명')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.user.username}"
    
    class Meta:
        verbose_name = '일일 작업 로그'
        verbose_name_plural = '일일 작업 로그'
