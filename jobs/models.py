from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django_countries.fields import CountryField # Import CountryField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    # Add description or icon fields if needed later

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'), # Consider if 'Remote' is a type or a location attribute
    )

    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs_posted', limit_choices_to={'user_type': 'company'})
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    # location = models.CharField(max_length=150) # Removed old location field
    country = CountryField(blank_label='(selectează țara)', default='RO') # Added country field, default Romania
    city = models.CharField("Oraș", max_length=100) # Added city field
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='RON', blank=True) # E.g., RON, EUR
    is_published = models.BooleanField(default=True) # Allow drafts or admin approval later
    is_featured = models.BooleanField(default=False) # For premium/featured listings
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add application deadline, required skills, experience level etc. later

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.companyprofile.company_name}" # Assumes CompanyProfile exists
