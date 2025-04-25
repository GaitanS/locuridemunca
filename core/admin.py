from django.contrib import admin
from .models import NewsletterSubscription, ContactMessage # Import models

# Register your models here.

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    list_filter = ('subscribed_at',)
    readonly_fields = ('subscribed_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'sent_at', 'is_read')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'sent_at') # Messages shouldn't be edited in admin
    list_editable = ('is_read',) # Allow marking as read
