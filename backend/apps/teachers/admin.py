from django.contrib import admin
from apps.teachers.models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience_years')
    search_fields = ('name', 'specialization')
