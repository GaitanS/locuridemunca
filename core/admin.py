from django.contrib import admin
from .models import ContactMessage, NewsletterSubscription, ContactInfo, FAQ, Article # Import all models

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

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'is_featured', 'created_at', 'published_at')
    list_filter = ('is_published', 'is_featured', 'created_at', 'author')
    list_editable = ('is_published', 'is_featured')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    
    fieldsets = (
        ('Conținut', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Setări publicare', {
            'fields': ('author', 'is_published', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Dacă este un articol nou
            obj.author = request.user
        super().save_model(request, obj, form, change)
