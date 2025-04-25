from django.contrib import admin
from .models import Project, Task, DailyWorkLog

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'start_date', 'end_date')
    search_fields = ('name', 'manager__username')
    inlines = [TaskInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'assignee', 'progress', 'status', 'start_date', 'end_date')
    list_filter = ('project', 'status', 'assignee')
    search_fields = ('name', 'description', 'project__name', 'assignee__username')

@admin.register(DailyWorkLog)
class DailyWorkLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'user')
    list_filter = ('date', 'user')
