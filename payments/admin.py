from django.contrib import admin
from .models import SubscriptionPlan # Corrected model name import

# Register your models here.

@admin.register(SubscriptionPlan) # Corrected model name
class PlanAdmin(admin.ModelAdmin): # Keep class name for consistency or rename if preferred
    # Updated list_display with new fields
    list_display = (
        'name',
        'price',
        'currency',
        'max_active_jobs',
        'visibility_days',
        'has_cv_access',
        'promoted_jobs_limit',
        'has_priority_support',
        'is_featured',
        'is_promoted_only',
        'is_active',
        'slug'
    )
    # Updated list_filter with new boolean fields
    list_filter = ( # Ensure these fields exist on SubscriptionPlan
        'is_active',
        'is_featured',
        'is_promoted_only',
        'has_cv_access',
        'has_priority_support'
    )
    search_fields = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    # Updated list_editable with new relevant fields
    list_editable = (
        'price',
        'currency',
        'max_active_jobs',
        'visibility_days',
        'has_cv_access',
        'promoted_jobs_limit',
        'has_priority_support',
        'is_featured',
        'is_promoted_only',
        'is_active'
    )
    # Ensure fields in list_editable exist on SubscriptionPlan
