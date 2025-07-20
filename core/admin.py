from django.contrib import admin
from .models import ContactMessage, NewsletterSubscription, ContactInfo, FAQ # Import all models

# Register your models here.

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'sent_at')

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('contact_type', 'title', 'description', 'is_active', 'order')
    list_filter = ('contact_type', 'is_active')
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'description', 'content')
    fieldsets = (
        ('Informații de bază', {
            'fields': ('contact_type', 'title', 'description', 'content')
        }),
        ('Stilizare', {
            'fields': ('icon_class', 'color_class')
        }),
        ('Setări', {
            'fields': ('is_active', 'order')
        }),
    )

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active', 'order')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Conținut', {
            'fields': ('question', 'answer')
        }),
        ('Setări', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
