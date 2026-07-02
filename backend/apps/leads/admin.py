import csv
from django.http import HttpResponse
from django.contrib import admin
from apps.leads.models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'course_interest', 'city', 'created_at')
    list_filter = ('course_interest', 'city')
    search_fields = ('name', 'phone', 'email')
    actions = ['export_as_csv']
    
    @admin.action(description='Export selected leads to CSV')
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response
