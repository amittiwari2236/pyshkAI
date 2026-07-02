from django.contrib import admin
from apps.schedules.models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'batch_type', 'class_mode', 'start_date')
    list_filter = ('batch_type', 'class_mode')
