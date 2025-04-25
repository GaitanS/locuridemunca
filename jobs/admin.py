from django.contrib import admin
from .models import Category, Job, JobReport, Application # Import JobReport and Application

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'city', 'country', 'job_type', 'is_published', 'created_at') # Replaced location with city, country
    list_filter = ('is_published', 'job_type', 'category', 'country', 'created_at') # Added country filter
    search_fields = ('title', 'description', 'company__username', 'company__companyprofile__company_name', 'city', 'country') # Replaced location with city, country
    raw_id_fields = ('company', 'category') # Better UI for selecting foreign keys
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at', 'status')
    list_filter = ('status', 'applied_at', 'job__category')
    search_fields = ('job__title', 'applicant__username', 'applicant__email')
    raw_id_fields = ('job', 'applicant')
    date_hierarchy = 'applied_at'
    ordering = ('-applied_at',)

@admin.register(JobReport)
class JobReportAdmin(admin.ModelAdmin):
    list_display = ('job', 'reporter_info', 'reason_summary', 'reported_at', 'status')
    list_filter = ('status', 'reported_at')
    search_fields = ('job__title', 'reporter__username', 'reason', 'admin_notes')
    list_editable = ('status',)
    raw_id_fields = ('job', 'reporter')
    date_hierarchy = 'reported_at'
    ordering = ('-reported_at',)

    @admin.display(description='Reporter')
    def reporter_info(self, obj):
        if obj.reporter:
            return obj.reporter.username
        return "Anonymous"

    @admin.display(description='Reason (Summary)')
    def reason_summary(self, obj):
        return (obj.reason[:75] + '...') if len(obj.reason) > 75 else obj.reason
