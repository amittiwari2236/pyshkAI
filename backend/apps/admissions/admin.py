from django.contrib import admin
from apps.admissions.models import Admission

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('course', 'start_date', 'end_date')
    list_filter = ('start_date',)
