from django.contrib import admin
from apps.courses.models import Course, FeeStructure

class FeeStructureInline(admin.StackedInline):
    model = FeeStructure

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration')
    search_fields = ('name',)
    inlines = [FeeStructureInline]
