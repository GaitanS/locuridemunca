from django.contrib import admin
from .models import Category, Job

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
