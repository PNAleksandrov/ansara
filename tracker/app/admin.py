from django.contrib import admin

from app.models import Task, CustomUser, TaskStatusHistory


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(TaskStatusHistory)
class TaskStatusHistoryAdmin(admin.ModelAdmin):
    pass