from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobSeekerProfile, CompanyProfile # Import profile models

# Register your models here.

# Use UserAdmin for the custom User model to get the standard user management interface
admin.site.register(User, UserAdmin)

# Register profile models
admin.site.register(JobSeekerProfile)

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'city', 'country', 'industry', 'plan', 'slug')
    search_fields = ('company_name', 'user__username', 'city', 'industry')
    list_filter = ('industry', 'country', 'plan')
    prepopulated_fields = {'slug': ('company_name',)}
    fieldsets = (
        (None, {
            'fields': ('user', 'company_name', 'slug')
        }),
        ('Contact & Location Information', {
            'fields': ('street_address', 'city', 'country', 'location', 'website')
        }),
        ('Company Details', {
            'fields': ('industry', 'description', 'logo')
        }),
        ('Subscription', {
            'fields': ('plan',)
        }),
    )

admin.site.register(CompanyProfile, CompanyProfileAdmin)
