from django.db import models
from django.utils import timezone # Import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} ({self.email}) - Subject: {self.subject}"

    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

class ContactInfo(models.Model):
    CONTACT_TYPE_CHOICES = [
        ('phone', 'Telefon'),
        ('email', 'Email'),
        ('location', 'Locație'),
        ('schedule', 'Program'),
    ]
    
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    content = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Clasa CSS pentru iconul FontAwesome (ex: fas fa-phone)")
    color_class = models.CharField(max_length=50, help_text="Clasa CSS pentru culoarea gradient (ex: from-blue-400 to-blue-600)")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Ordinea de afișare")
    
    def __str__(self):
        return f"{self.get_contact_type_display()} - {self.title}"
    
    class Meta:
        ordering = ['order', 'contact_type']
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Information"

class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name="Întrebare")
    answer = models.TextField(verbose_name="Răspuns")
    is_active = models.BooleanField(default=True, verbose_name="Activ")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordinea de afișare")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titlu")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, verbose_name="Rezumat", help_text="Scurt rezumat al articolului (max 300 caractere)")
    content = models.TextField(verbose_name="Conținut")
    featured_image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Imagine principală")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles', verbose_name="Autor")
    is_published = models.BooleanField(default=False, verbose_name="Publicat")
    is_featured = models.BooleanField(default=False, verbose_name="Articol evidențiat", help_text="Articolele evidențiate apar pe prima pagină")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Creat la")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizat la")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Publicat la")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:article_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Articol"
        verbose_name_plural = "Articole"

# Add other core models here if needed
