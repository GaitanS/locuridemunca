from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobSeekerProfile, CompanyProfile # Import profile models

# Register your models here.

# Use UserAdmin for the custom User model to get the standard user management interface
admin.site.register(User, UserAdmin)

# Register profile models
admin.site.register(JobSeekerProfile)
admin.site.register(CompanyProfile)
